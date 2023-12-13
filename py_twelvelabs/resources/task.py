from py_twelvelabs.models import Task
from py_twelvelabs.exceptions import APIRequestError, InsufficientParametersError


class TaskResource:
    def __init__(self, client):
        self.client = client

    def create(self, index_id: str, video_file: str = None, video_url: str = None, language: str = "en", provide_transcription: bool = False, transcription_file: str = None, transcription_url: str = None, disable_video_stream: bool = False):
        """
        Create a task.

        :param index_id: Index ID.
        :param video_file: Video file. Either video_file or video_url must be provided.
        :param video_url: Video URL. Either video_file or video_url must be provided.
        :param language: Language.
        :param provide_transcription: Provide transcription.
        :param transcription_file: Transcription file.
        :param transcription_url: Transcription URL.
        :param disable_video_stream: Disable video stream.
        :return: Task ID.
        """

        if video_file is None and video_url is None:
            raise InsufficientParametersError("Video file or URL must be provided.")

        data = {
            "index_id": index_id,
            "language": language,
            "provide_transcription": provide_transcription,
            "disable_video_stream": disable_video_stream,
        }

        if video_file is not None:
            data['video_file'] = video_file
        if video_url is not None:
            data['video_url'] = video_url
        if transcription_file is not None:
            data['transcription_file'] = transcription_file
        if transcription_url is not None:
            data['transcription_url'] = transcription_url

        response = self.client.submit_multi_part_request("tasks", method="POST", data=data)
        result = response.json()
        if response.status_code == 200:
            return result['_id']
        else:
            raise APIRequestError(f"Failed to create task: {result['message']}")
        
    def get(self, task_id: str) -> Task:
        """
        Get a task.

        :param task_id: Task ID.
        :return: Task.
        """
        
        response = self.client.submit_request(f"tasks/{task_id}")
        result = response.json()
        if response.status_code == 200:
            return Task(**result)
        else:
            raise APIRequestError(f"Failed to get task {task_id}: {result['message']}")
        
    def delete(self, task_id: str):
        """
        Delete a task.

        :param task_id: Task ID.
        :return: True if successful.
        """

        response = self.client.submit_request(f"tasks/{task_id}", method="DELETE")
        if response.status_code == 204:
            return True
        else:
            result = response.json()
            raise APIRequestError(f"Failed to delete task {task_id}: {result['message']}")
