from prometheus_client import Counter, Histogram

GRPC_DURATION = Histogram("grpc_requests_duration_seconds",
                          "gRPC request latency",
                          ["service", "method", "status"])

GRPC_COUNT = Counter("grpc_requests_total",
                     "Total gRPC requests",
                     ["service", "method", "status"])