using ServiceStack;
using DataDog.TechnicalTest.ServiceModel.ServiceModels;
using Datadog.Trace;

namespace DataDog.TechnicalTest.ServiceInterface
{
    public class MyServices : Service
    {
        public object Any(Entry request)
        {
            using (var scope = Tracer.Instance.StartActive("web.request"))
            {
                var span = scope.Span;
                span.Type = SpanTypes.Web;
                span.ResourceName = Request.AbsoluteUri;
                span.SetTag(Tags.HttpMethod, "GET");
                return new StringResponse { Result = "Entrypoint to the Application" };
            }
        }

        public object Any(ApmEndpoint request)
        {
            using (var scope = Tracer.Instance.StartActive("web.request"))
            {
                var span = scope.Span;
                span.Type = SpanTypes.Web;
                span.ResourceName = Request.AbsoluteUri;
                span.SetTag(Tags.HttpMethod, "GET");
                return new StringResponse { Result = "Getting APM Started" };
            }
        }

        public object Any(TraceEndpoint request)
        {
            using (var scope = Tracer.Instance.StartActive("web.request"))
            {
                var span = scope.Span;
                span.Type = SpanTypes.Web;
                span.ResourceName = Request.AbsoluteUri;
                span.SetTag(Tags.HttpMethod, "GET");
                return new StringResponse { Result = "Posting Traces" };
            }
        }
    }
}