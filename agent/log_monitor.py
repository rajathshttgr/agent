import asyncio
import os
from .log_parser import LogParser
from .critical_logs import process_critical_event
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "logs" / "app.log"


class LogMonitor:
    def __init__(self, queue: asyncio.Queue, stop_event: asyncio.Event):
        self.queue = queue
        self.stop_event = stop_event

    async def start(self):
        print("Log monitor started...")

        try:
            with open(LOG_FILE, "r") as f:
                f.seek(0, os.SEEK_END)

                while not self.stop_event.is_set():
                    line = f.readline()

                    if not line:
                        await asyncio.sleep(0.2)
                        continue

                    await self.queue.put(line)

        except asyncio.CancelledError:
            print("Log monitor task cancelled")
            raise

        finally:
            print("Log monitor stopped gracefully")


async def worker(queue: asyncio.Queue, stop_event: asyncio.Event):
    parser = LogParser()

    print("Worker started...")

    try:
        while not stop_event.is_set():
            try:
                # timeout lets loop re-check stop_event periodically
                line = await asyncio.wait_for(queue.get(), timeout=0.5)
            except asyncio.TimeoutError:
                continue

            event = parser.process_line(line)

            if event:
                await process_critical_event(event)

    except asyncio.CancelledError:
        print("Worker task cancelled")
        raise

    finally:
        print("Worker stopped gracefully")
