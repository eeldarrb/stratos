import time
import queue
import threading
from watchdog import events
from watchdog.observers import Observer

from src.file_service import FileService


class MyEventHandler(events.FileSystemEventHandler):
    def __init__(self, event_queue):
        self.event_queue = event_queue

    def on_moved(self, event: events.DirMovedEvent | events.FileMovedEvent) -> None:
        self.event_queue.put(("moved", event.dest_path))

    def on_created(
        self, event: events.DirCreatedEvent | events.FileCreatedEvent
    ) -> None:
        self.event_queue.put(("created", event.src_path))

    def on_deleted(
        self, event: events.DirDeletedEvent | events.FileDeletedEvent
    ) -> None:
        self.event_queue.put(("deleted", event.src_path))


def worker(file_service: FileService, embed_queue: queue.Queue):
    try:
        while True:
            fs_event, file_path = embed_queue.get()
            if fs_event == "created" or fs_event == "moved":
                file_service.process_path(file_path)
            elif fs_event == "deleted":
                file_service.delete_file(file_path)
    except Exception as e:
        print(f"[Worker] Unexpected Error Occured: {e}")


def start_listener(file_service: FileService, paths_to_watch: list[str]):
    embed_queue = queue.Queue()
    event_handler = MyEventHandler(embed_queue)
    observer = Observer()

    thread = threading.Thread(
        target=worker, args=(file_service, embed_queue), daemon=True
    )
    thread.start()

    for path in paths_to_watch:
        observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
