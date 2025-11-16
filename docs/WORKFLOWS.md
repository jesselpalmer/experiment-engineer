# Workflow Orchestration Guide

## Overview

ExperimentKit's workflow system allows you to build multi-step experiment
processes that orchestrate multiple agents with dependencies, conditional
execution, and data flow between steps.

## Basic Concepts

### Workflow Steps

A workflow consists of multiple steps, where each step:
- Executes an agent
- Can depend on other steps
- Can have conditional execution
- Can use results from previous steps

### Step Dependencies

Steps can depend on other steps using `depends_on`:

```python
workflow.add_step(
    name="step2",
    agent_name="some_agent",
    depends_on=["step1"],  # Must run after step1
)
```

The workflow system automatically resolves dependencies using topological
sorting, so steps execute in the correct order.

### Data Flow Between Steps

Steps can reference results from previous steps using `$` syntax:

```python
workflow.add_step(
    name="step2",
    agent_name="analyzer",
    inputs={"data": "$step1"},  # Uses result from step1
)
```

You can also reference initial inputs:

```python
workflow.execute(initial_inputs={"hypothesis": "..."})
# In step definition:
inputs={"hypothesis": "$hypothesis"}  # References initial input
```

### Conditional Execution

Steps can have conditions that determine if they execute:

```python
workflow.add_step(
    name="optional_step",
    agent_name="some_agent",
    condition="$previous_step",  # Only run if previous_step succeeded
)
```

## Creating a Custom Workflow

### Simple Sequential Workflow

```python
from src.workflows.workflow import Workflow

class MyWorkflow(Workflow):
    def __init__(self):
        super().__init__("my_workflow")
        
        self.add_step(
            name="first",
            agent_name="agent1",
            inputs={"input": "$initial"},
        ).add_step(
            name="second",
            agent_name="agent2",
            inputs={"data": "$first"},
            depends_on=["first"],
        )
```

### Workflow with Branching

```python
class BranchingWorkflow(Workflow):
    def __init__(self):
        super().__init__("branching")
        
        # Common first step
        self.add_step(
            name="analyze",
            agent_name="analyzer",
            inputs={"data": "$input"},
        )
        
        # Branch A - only if analyze succeeds
        self.add_step(
            name="branch_a",
            agent_name="agent_a",
            inputs={"data": "$analyze"},
            depends_on=["analyze"],
            condition="$analyze",
        )
        
        # Branch B - always runs after analyze
        self.add_step(
            name="branch_b",
            agent_name="agent_b",
            inputs={"data": "$analyze"},
            depends_on=["analyze"],
        )
```

### Complex Multi-Step Workflow

```python
class ComplexWorkflow(Workflow):
    def __init__(self):
        super().__init__("complex_experiment")
        
        # Step 1: Initial processing
        self.add_step(
            name="preprocess",
            agent_name="preprocessor",
            inputs={"raw_data": "$input"},
        )
        
        # Step 2: Analysis (depends on preprocessing)
        self.add_step(
            name="analyze",
            agent_name="analyzer",
            inputs={"processed": "$preprocess"},
            depends_on=["preprocess"],
        )
        
        # Step 3: Validation (depends on analysis)
        self.add_step(
            name="validate",
            agent_name="validator",
            inputs={"analysis": "$analyze"},
            depends_on=["analyze"],
            condition="$analyze",  # Only if analysis succeeded
        )
        
        # Step 4: Final step (depends on validation)
        self.add_step(
            name="finalize",
            agent_name="finalizer",
            inputs={
                "analysis": "$analyze",
                "validation": "$validate",
            },
            depends_on=["validate"],
        )
```

## Executing Workflows

```python
workflow = MyWorkflow()
result = workflow.execute(initial_inputs={"initial": "some value"})

# Check status
if result.status.value == "completed":
    # Access step results
    step1_result = result.steps["first"]["result"]
    step2_result = result.steps["second"]["result"]
    final_result = result.final_result
else:
    print(f"Workflow failed: {result.error}")
```

## Current Limitations

The workflow system currently supports:
- ✅ Sequential step execution
- ✅ Step dependencies
- ✅ Basic conditional execution
- ✅ Data flow between steps
- ✅ Error handling per step

Future enhancements (not yet implemented):
- ⏳ True parallel execution
- ⏳ Advanced condition evaluation (expressions, comparisons)
- ⏳ Loops and iteration
- ⏳ Retry logic at workflow level
- ⏳ Step timeouts

## Best Practices

1. **Name steps clearly**: Use descriptive names for steps
2. **Define dependencies explicitly**: Always specify `depends_on` when a step
   needs previous results
3. **Handle errors**: Workflows stop on first failure - design with this in mind
4. **Use conditions wisely**: Conditions help create branching logic
5. **Test incrementally**: Build and test workflows step by step

## Examples

See `examples/custom_workflow.py` for a complete example of creating a custom
workflow.

