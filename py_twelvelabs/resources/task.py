import time
import mimetypes
from typing import Text, List

from py_twelvelabs.models import Task
from py_twelvelabs.settings import settings
from py_twelvelabs.utilities.logger import get_logger
from py_twelvelabs.exceptions import APIRequestError, InsufficientParametersError, TaskFailedError, TaskDeletionNotAllowedError


class TaskResource:
    def __init__(self, client):
        self.client = client
        self.logger = get_logger(__name__)

    def create_async(self, index_id: Text, video_file: Text = None, video_url: Text = None, language: Text = "en", provide_transcription: Text = "false", transcription_file: Text = None, transcription_url: Text = None, disable_video_stream: Text = "false"):
        """
        Create a task asynchronously.

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
            data['video_file'] = self._get_video_tuple(video_file)
        if video_url is not None:
            data['video_url'] = video_url
        if transcription_file is not None:
            data['transcription_file'] = transcription_file
        if transcription_url is not None:
            data['transcription_url'] = transcription_url

        response = self.client.submit_multi_part_request("tasks", method="POST", data=data)
        result = response.json()
        if response.status_code == 201:
            return result['_id']
        else:
            raise APIRequestError(f"Failed to create task: {result['message']}")
        
    def create_sync(self, index_id: Text, video_file: Text = None, video_url: Text = None, language: Text = "en", provide_transcription: Text = "false", transcription_file: Text = None, transcription_url: Text = None, disable_video_stream: Text = "false"):
        """
        Create a task synchronously.

        :param index_id: Index ID.
        :param video_file: Video file. Either video_file or video_url must be provided.
        :param video_url: Video URL. Either video_file or video_url must be provided.
        :param language: Language.
        :param provide_transcription: Provide transcription.
        :param transcription_file: Transcription file.
        :param transcription_url: Transcription URL.
        :param disable_video_stream: Disable video stream.
        :return: Task.
        """

        task_id = self.create_async(index_id, video_file, video_url, language, provide_transcription, transcription_file, transcription_url, disable_video_stream)

        is_task_running = True

        while is_task_running:
            task = self.get(task_id)
            task_status = task.status
            self.logger.info(f"Task {task_id} is in the {task_status} state.")

            wait_durtion = task['process']['remain_seconds'] if 'process' in task else settings.TASK_STATUS_POLLING_INTERVAL

            if task_status in ('pending', 'indexing', 'validating'):
                self.logger.info(f"Task {task_id} will be polled again in {wait_durtion} seconds.")
                time.sleep(wait_durtion)

            elif task_status == 'ready':
                self.logger.info(f"Task {task_id} completed successfully.")
                is_task_running = False

            else:
                raise TaskFailedError(f"Task {task_id} failed with status {task_status}.")
            
        return task

    def _get_video_tuple(self, video_file):
        return (video_file, open(video_file, "rb"), mimetypes.guess_type(video_file )[0])
        
    def get(self, task_id: Text) -> Task:
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
        
    def list(self, page: int = 1, page_limit: Text = 10, sort_by: Text = "created_at", sort_option: Text = "desc", _id: Text = None, index_id: Text = None, filename: Text = None, duration: int = None, width: int = None, height: int = None, created_at: Text = None, updated_at: Text = None, estimated_time: Text = None) -> List[Task]:
        """
        List tasks.

        :param page: Page number.
        :param page_limit: Page limit.
        :param sort_by: Sort by.
        :param sort_option: Sort option.
        :param _id: Task ID.
        :param index_id: Index ID.
        :param filename: Filename.
        :param duration: Duration.
        :param width: Width.
        :param height: Height.
        :param created_at: Created at.
        :param updated_at: Updated at.
        :param estimated_time: Estimated time.
        :return: List of Tasks.
        """

        params = {
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "_id": _id,
            "index_id": index_id,
            "filename": filename,
            "duration": duration,
            "width": width,
            "height": height,
            "created_at": created_at,
            "updated_at": updated_at,
            "estimated_time": estimated_time,
        }

        response = self.client.submit_request("tasks", params=params)
        result = response.json()
        if response.status_code == 200:
            return [Task(**task) for task in result['data']]
        else:
            raise APIRequestError(f"Failed to list tasks: {result['message']}")
        
    def delete(self, task_id: Text):
        """
        Delete a task.

        :param task_id: Task ID.
        :return: True if successful.
        """

        response = self.client.submit_request(f"tasks/{task_id}", method="DELETE")
        # TODO: if the status of the task is 'ready', the video vector must be deleted first
        if response.status_code == 204:
            return True
        elif response.status_code == 409:
            self.logger.error(f"Failed to delete task {task_id}: {response.json()['message']}")
            raise TaskDeletionNotAllowedError("Only tasks with status 'ready' or 'failed' can be deleted.")
        else:
            result = response.json()
            raise APIRequestError(f"Failed to delete task {task_id}: {result['message']}")
