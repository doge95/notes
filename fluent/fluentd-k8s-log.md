# Collect Application Logs using Fluentd in Kubernetes
Use the official [fluentd chart](https://github.com/fluent/helm-charts/tree/fluentd-0.3.9).  
Container runtime - `containerd`.  
Fluentd deployment mode - `daemonset`.
```
fileConfigs:
  01_sources.conf: |-
    <source>
      @type tail
      @id in_tail_container_logs
      path /var/log/containers/*.log
      pos_file /var/log/fluentdseacloud/containers.log.pos
      tag raw.kubernetes.*
      read_from_head true
      follow_inodes true
      refresh_interval 1
      read_bytes_limit_per_second 500000
      <parse>
        @type regexp
        expression /^(?<time>.+) (?<@stream>stdout|stderr) (?<logtag>[FP]) (?<message>.*)$/
        time_format %Y-%m-%dT%H:%M:%S.%L%z
        keep_time_key false
      </parse>
      emit_unmatched_lines true
    </source>

  02_filters.conf: |-
    <match raw.**>
      @type detect_exceptions
      remove_tag_prefix raw
      languages all
      max_bytes 500000
      max_lines 1000
      multiline_flush_interval 0.1
    </match>

    <filter kubernetes.**>
      @type kubernetes_metadata
      @id filter_kube_metadata
      skip_labels false
      skip_container_metadata true
      skip_namespace_metadata true
      skip_master_url true
    </filter>

    <filter kubernetes.**>
      @type record_modifier
      <record>
        message ${record["message"]}
        product ${record.dig("kubernetes", "labels", "product")}
        namespace ${record.dig("kubernetes", "namespace_name")}
        hostname ${record.dig("kubernetes", "host")}
        pod ${record.dig("kubernetes", "pod_name")}
        container ${record.dig("kubernetes", "container_name")}
      </record>
      remove_keys kubernetes, docker, logtag, message
    </filter>

    <match kubernetes.**>
      @type rewrite_tag_filter
      <rule>
        key product
        pattern /^$/
        tag clear
      </rule>
      <rule>
        key product
        pattern /^(.+)$/
        tag applog
      </rule>
    </match>

    <filter applog.**>
      @type parser
      key_name message
      reserve_data true
      remove_key_name_field true
      <parse>
        @type multi_format
        <pattern>
          format json
          time_key time
          keep_time_key true
          time_format %Y-%m-%dT%H:%M:%S%Z
        </pattern>
        <pattern>
          format regexp
          expression /^(?<time>\S*)\|(?<level>\S*)\|(?<message>[^ ].*)$/
          time_key time
          keep_time_key true
          time_format %Y-%m-%dT%H:%M:%S%Z
        </pattern>
        <pattern>
          format none
          message_key message
        </pattern>
      </parse>
    </filter>

    <match clear raw.**>
      @type null
    </match>

  04_outputs.conf: |-
    <match **>
      @type copy 
      <store>
        @type stdout 
      </store>
      # Send logs to Kafka
      <store>
        @type kafka2
        brokers <broker-endpoint>
        topic_key topic
        ssl_ca_cert /home/fluent/ssl/ca.crt
        ssl_client_cert /home/fluent/ssl/user.crt
        ssl_client_cert_key /home/fluent/ssl/user.key
        max_send_retries 3
        <inject>
          time_key time
          time_type string
          time_format %Y-%m-%dT%H:%M:%S%Z
        </inject>
        <format>
          @type json
        </format>
        <buffer topic>
          @type memory
          flush_interval 3s
          retry_max_times 10
        </buffer>
      </store>
      # Send logs to OpenSearch; index template & policy must exist.
      <store>
        @type elasticsearch_data_stream
        data_stream_name logs-${tag}
        data_stream_template_name logs-template
        data_stream_ilm_name logs-policy
        hosts <endpoint>
        user admin
        password <password>
        ssl_verify false
        ssl_version TLSv1_2
        reload_connections false
        reconnect_on_error true
        reload_on_failure true
        log_es_400_reason false
        request_timeout 1000s
        time_key time
        include_timestamp true
        remove_keys topic, module, project_id, id, product, time
        <buffer>
          @type memory
          flush_interval 3s
          retry_max_times 10
        </buffer>
      </store>
      # Send logs to Elasticsearch   
      <store>           
        @type elasticsearch_data_stream
        data_stream_name ${tag}
        hosts <endpoint>
        user elastic
        password <password>
        ssl_verify false
        reload_connections false
        reconnect_on_error true
        reload_on_failure true
        log_es_400_reason false
        request_timeout 1000s
        include_timestamp true
        <buffer>
          @type memory
          flush_interval 3s
          retry_max_times 10
        </buffer>
      </store>
    </match>
```