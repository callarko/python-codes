import azure.durable_functions as df

def orchestrator_function(context: df.DurableOrchestrationContext):
    result = yield context.call_activity('Hello', "world")
    return result

main = df.Orchestrator.create(orchestrator_function)
