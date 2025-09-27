import time
from watchdog import events
from watchdog.observers import Observer


class MyEventHandler(events.FileSystemEventHandler):
    def on_moved(self, event: events.DirMovedEvent | events.FileMovedEvent) -> None:
        print("moved")
        print(event)

    def on_created(
        self, event: events.DirCreatedEvent | events.FileCreatedEvent
    ) -> None:
        print("created")
        print(event)

    def on_deleted(
        self, event: events.DirDeletedEvent | events.FileDeletedEvent
    ) -> None:
        print("deleted")
        print(event)


def start_listener(paths_to_watch: list[str]):
    event_handler = MyEventHandler()
    observer = Observer()

    for path in paths_to_watch:
        observer.schedule(event_handler, path, recursive=True)

    observer.start()

    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
