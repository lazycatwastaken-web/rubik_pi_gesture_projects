from __future__ import annotations

import queue
import subprocess
import threading


class MatterPlug:
    def __init__(
        self,
        node_id: int = 1,
        endpoint_id: int = 1,
        storage_directory: str = (
            "/home/ubuntu/snap/chip-tool/common/storage"
        ),
    ) -> None:
        self.chip_tool = "/snap/bin/chip-tool"
        self.node_id = str(node_id)
        self.endpoint_id = str(endpoint_id)
        self.storage_directory = storage_directory

        self._queue: queue.Queue[bool] = queue.Queue(maxsize=1)
        self._requested_state: bool | None = None
        self._lock = threading.Lock()

        self._worker_thread = threading.Thread(
            target=self._worker,
            daemon=True,
        )
        self._worker_thread.start()

    def turn_on(self) -> None:
        self.set_power(True)

    def turn_off(self) -> None:
        self.set_power(False)

    def set_power(self, turn_on: bool) -> None:
        with self._lock:
            if turn_on == self._requested_state:
                return

            self._requested_state = turn_on

        # Discard an older command that has not started.
        try:
            self._queue.get_nowait()
            self._queue.task_done()
        except queue.Empty:
            pass

        try:
            self._queue.put_nowait(turn_on)
        except queue.Full:
            pass

    def _build_command(self, turn_on: bool) -> list[str]:
        return [
            self.chip_tool,
            "onoff",
            "on" if turn_on else "off",
            self.node_id,
            self.endpoint_id,
            "--storage-directory",
            self.storage_directory,
        ]

    def _worker(self) -> None:
        while True:
            turn_on = self._queue.get()
            command = self._build_command(turn_on)

            print(
                "Running Matter command:",
                " ".join(command),
                flush=True,
            )

            try:
                result = subprocess.run(
                    command,
                    text=True,
                    capture_output=True,
                    timeout=40,
                    check=False,
                )

                if result.returncode == 0:
                    state = "ON" if turn_on else "OFF"
                    print(f"Matter plug successfully turned {state}")

                else:
                    print(
                        "Matter plug command failed "
                        f"with exit code {result.returncode}"
                    )

                    # chip-tool may write useful logs to either stream.
                    if result.stdout.strip():
                        print("chip-tool stdout:")
                        print(result.stdout[-5000:])

                    if result.stderr.strip():
                        print("chip-tool stderr:")
                        print(result.stderr[-5000:])

                    with self._lock:
                        if self._requested_state == turn_on:
                            self._requested_state = None

            except subprocess.TimeoutExpired as error:
                print("Matter plug command timed out")

                if error.stdout:
                    print("Partial stdout:")
                    print(error.stdout)

                if error.stderr:
                    print("Partial stderr:")
                    print(error.stderr)

                with self._lock:
                    if self._requested_state == turn_on:
                        self._requested_state = None

            except Exception as error:
                print(f"Matter plug exception: {error}")

                with self._lock:
                    if self._requested_state == turn_on:
                        self._requested_state = None

            finally:
                self._queue.task_done()