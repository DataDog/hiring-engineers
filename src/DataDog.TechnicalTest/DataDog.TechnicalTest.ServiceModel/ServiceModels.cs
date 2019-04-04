using ServiceStack;

namespace DataDog.TechnicalTest.ServiceModel.ServiceModels
{
    [Route("/entry")]
    public class Entry : IReturn<StringResponse>
    { }

    [Route("/api/apm")]
    public class ApmEndpoint : IReturn<StringResponse>
    { }

    [Route("/api/trace")]
    public class TraceEndpoint : IReturn<StringResponse>
    { }

    public class StringResponse
    {
        public string Result { get; set; }
    }
}