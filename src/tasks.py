from celery import Celery
import docker
import json

app = Celery('tasks', broker='redis://localhost:6379/0')

client = docker.from_env()


@app.task
def evaluate_code_in_docker(user_code):
    try:
        container = client.containers.run(
            image='user-code-runner',
            stdin_open=True,
            detach=True,
            mem_limit='128m',  # メモリ制限
            nano_cpus=1 * 10**9, # CPU制限（1 CPU）
        )
        container.put_archive('/', tar_archive_of_code(user_code))  
        response = container.exec_run('python /run_user_code.py', stdin=True, tty=True)
        output = json.loads(response.output.decode('utf-8'))
        container.remove()
        return output
    except Exception as e:
        return {"status": "error", "error": str(e)}

def tar_archive_of_code(code):
    import tarfile
    import io
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        info = tarfile.TarInfo(name='user_code.py')
        info.size = len(code)
        tar.addfile(tarinfo=info, fileobj=io.BytesIO(code.encode('utf-8')))
    tar_stream.seek(0)
    return tar_stream
