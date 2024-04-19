# Kelpie Demo

This a a toy example of a long running job to demonstrate how to make your job compatible with kelpie.

## The "job"

The job counts to 50, with a 5 second sleep between steps. Break out the super computers. However, it demonstrates how to structure a job to take advantage of Kelpie.

### Environment Variables

The job [accepts the environment variables]((https://github.com/SaladTechnologies/kelpie-demo/blob/main/main.py#L5-L7)) set by kelpie

```python
import os

input_dir = os.getenv('INPUT_DIR')
output_dir = os.getenv('OUTPUT_DIR')
checkpoint_dir = os.getenv('CHECKPOINT_DIR')
```

### Tries to Resume

The job [tries to resume from a checkpoint](https://github.com/SaladTechnologies/kelpie-demo/blob/main/main.py#L28-L35) in the checkpoint directory before starting from the beginning.

```python
checkpoint_file = os.path.join(checkpoint_dir, 'count.txt')

try:
    with open(checkpoint_file, 'r') as f:
        current_count = int(f.read())
        print(f'Resuming from {current_count}', flush=True)
except FileNotFoundError:
    current_count = 0
```

### Saves its progress

The job [saves its progress](https://github.com/SaladTechnologies/kelpie-demo/blob/main/main.py#L38-L42) to the checkpoint directory after a chunk of "work".

```python
print(f'Processing {current_count}', flush=True)
time.sleep(5) # The "work"
current_count += 1
with open(checkpoint_file, 'w') as f:
    f.write(str(current_count))
```

### Saves its output

The job [saves its output](https://github.com/SaladTechnologies/kelpie-demo/blob/main/main.py#L44-L46) in the output directory when it is completed

```python
with open(os.path.join(output_dir, 'result.txt'), 'w') as f:
    print(f'Processed {current_count} records', flush=True)
    f.write(f'Processed {current_count} records')
```

### Exits normally

The [job exits normally](https://github.com/SaladTechnologies/kelpie-demo/blob/main/main.py#L48), with the default exit code of 0.

### Building the job

This job is built from [Dockerfile.base](https://github.com/SaladTechnologies/kelpie-demo/blob/main/Dockerfile.base).

### Adding Kelpie

Kelpie is added to the image *on top* of the base image in [Dockerfile.kelpie](https://github.com/SaladTechnologies/kelpie-demo/blob/main/Dockerfile.kelpie).

And then when running the container, you add some environment variables that are specific to kelpie, and some that are for your s3-compatible storage. You can see an example in [docker-compose.yml](https://github.com/SaladTechnologies/kelpie-demo/blob/main/docker-compose.yml)