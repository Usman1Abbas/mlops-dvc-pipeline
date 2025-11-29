import kfp
from kfp import dsl

# Load components
load_data_op = kfp.components.load_component_from_file('components/load_data.yaml')
preprocess_data_op = kfp.components.load_component_from_file('components/preprocess_data.yaml')
train_model_op = kfp.components.load_component_from_file('components/train_model.yaml')
evaluate_model_op = kfp.components.load_component_from_file('components/evaluate_model.yaml')

@dsl.pipeline(
    name='Boston Housing Pipeline',
    description='A simple pipeline to train and evaluate a model on Boston Housing data.'
)
def ml_pipeline():
    # Step 1: Load Data
    load_task = load_data_op()
    
    # Step 2: Preprocess Data
    preprocess_task = preprocess_data_op(
        input_data=load_task.output
    )
    
    # Step 3: Train Model
    train_task = train_model_op(
        train_data=preprocess_task.outputs['train_data']
    )
    
    # Step 4: Evaluate Model
    evaluate_task = evaluate_model_op(
        test_data=preprocess_task.outputs['test_data'],
        model=train_task.output
    )

if __name__ == '__main__':
    kfp.compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
