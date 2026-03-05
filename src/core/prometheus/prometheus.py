import time
import grpc

from src.core.prometheus.prometheus_metrics import GRPC_COUNT, GRPC_DURATION


class MetricsInterceptor(grpc.aio.ServerInterceptor):
    service_name = "auth-service"

    async def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        
        start = time.perf_counter()
        try:
            response = await continuation(handler_call_details)
            duration = time.perf_counter() - start

            GRPC_DURATION.labels(
                service=self.service_name,
                method=method,
                status="ok"
            ).observe(duration)

            GRPC_COUNT.labels(
                service=self.service_name,
                method=method,
                status="ok"
            ).inc()
            return response
        except Exception:
            duration = time.perf_counter() - start

            GRPC_DURATION.labels(
                service=self.service_name,
                method=method,
                status="error"
            ).observe(duration)

            GRPC_COUNT.labels(
                service=self.service_name,
                method=method,
                status="error"
            ).inc()

            raise

                