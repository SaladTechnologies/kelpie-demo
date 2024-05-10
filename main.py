import os
import signal
import time

input_dir = os.getenv('INPUT_DIR', "/input")
output_dir = os.getenv('OUTPUT_DIR', "/output")
checkpoint_dir = os.getenv('CHECKPOINT_DIR', "/checkpoint")
max_count = int(os.getenv('MAX_COUNT', "50"))

if not input_dir or not output_dir or not checkpoint_dir:
    raise ValueError('INPUT_DIR, OUTPUT_DIR, and CHECKPOINT_DIR must be set')

os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
os.makedirs(checkpoint_dir, exist_ok=True)

keep_alive = True


def signal_handler(sig, frame):
    global keep_alive
    keep_alive = False


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

checkpoint_file = os.path.join(checkpoint_dir, 'count.txt')

try:
    with open(checkpoint_file, 'r') as f:
        current_count = int(f.read())
        print(f'Resuming from {current_count}', flush=True)
except FileNotFoundError:
    current_count = 0

while keep_alive and current_count < max_count:
    print(f'Processing {current_count}', flush=True)
    time.sleep(5)
    current_count += 1
    with open(checkpoint_file, 'w') as f:
        f.write(str(current_count))

with open(os.path.join(output_dir, 'result.txt'), 'w') as f:
    print(f'Processed {current_count} records', flush=True)
    f.write(f'Processed {current_count} records')

print('Done', flush=True)
