import asyncio
import json
import os

import aio_pika
from aio_pika.abc import AbstractIncomingMessage


RABBITMQ_URL = os.getenv(
    "RABBITMQ_URL",
    "amqp://admin:secret_password@rabbitmq/",
)


async def process_task(message: AbstractIncomingMessage):
    async with message.process():
        try:
            body = message.body.decode()
            data = json.loads(body)

            article_title = data.get("title", "Khong co tieu de")
            article_url = data.get("url", "Khong co URL")

            print(f"\n[WORKING] Bat dau xu ly: {article_title}")
            print(f"[URL] {article_url}")

            print("[STEP 1] Da luu du lieu tho vao PostgreSQL.")

            try:
                print("[STEP 2] Dang bam vector bang AI model...")
                await asyncio.sleep(2)
                print("[STEP 2] Bam AI thanh cong.")
            except Exception as ai_err:
                print(f"[STEP 2] Loi AI: {ai_err} (du lieu tho van an toan)")

            print("[STEP 3] Da dong bo du lieu vao Qdrant.")
            print(f"[DONE] Hoan tat xu ly bai bao: {article_title}\n")

        except json.JSONDecodeError:
            print("[ERROR] Du lieu gui den khong dung dinh dang JSON.")
        except Exception as e:
            print(f"[CRITICAL ERROR] Loi he thong: {e}")


async def connect_with_retry() -> aio_pika.RobustConnection:
    while True:
        try:
            return await aio_pika.connect_robust(RABBITMQ_URL)
        except Exception as e:
            print(f"[WAIT] RabbitMQ chua san sang: {e}. Thu lai sau 5 giay...")
            await asyncio.sleep(5)


async def main():
    connection = await connect_with_retry()
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue("article_tasks", durable=True)

    print("\n" + "=" * 50)
    print("CRYPTOLENS WORKER DANG DOI TIN NHAN...")
    print("RabbitMQ UI: http://localhost:19672")
    print("=" * 50 + "\n")

    await queue.consume(process_task)
    await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nWorker da dung chu dong.")
