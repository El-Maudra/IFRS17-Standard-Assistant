import os
from dotenv import load_dotenv
import openai, requests, json, time, logging
from datetime import datetime

# Load environment variables
load_dotenv()

client = openai.OpenAI()


# Step 1: Upload a file to Open AI embeddings
vector_store = client.beta.vector_stores.create(name="IFRS 17 Standard")

filepath = ["./IFRS17.pdf"]
file_streams = [open(path, "rb") for path in filepath]
file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
  vector_store_id=vector_store.id, files=file_streams
)


# Step 2: Create an assistant
assistant = client.beta.assistants.create(
    name="IFRS 17 Assistant",
    instructions = """You are a helpful study assistant who knows a lot about understanding IFRS 17 Standard by IASB. Your role is to summarize standard, clarify terminology within context, and extract key information and formulas. Cross-reference information for additional insights and answer related questions comprehensively. Analyze the standard, key changes and where applicable. Respond to queries effectively, incorporating feedback to enhance your accuracy. Handle data securely and update your knowledge base with the latest standards and any similar research on the same. Adhere to ethical standards, respect intellectual property, and provide users with guidance on the standard. Maintain a feedback loop for continuous improvement and user support. Your ultimate goal is to facilitate a deeper understanding of complex IFRS 17 Standard material, making it more accessible and comprehensible.""",
    tools = [{"type": "file_search"}],
    model="gpt-3.5-turbo",
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)

# Get the Assistant ID
# assis_id = assistant.id
# print(assis_id)

# Hardcoded ids to be used once the first code run is done and the assistant was created
thread_id = "thread_YqVX9wUSUq9kD3rhUX1o8ejf"
assis_id = "asst_SkhrTGeZLM1fksLtDUo9BVRQ"

# == Step 3. Create a Thread
message_cont = "What is IFRS 17?"
message = client.beta.threads.messages.create(
    thread_id=thread_id,
    role="user", 
    content=message_cont
)

# thread = client.beta.threads.create()
# thread_id = thread.id
# print(thread_id)

# message = client.beta.threads.messages.create(
#     thread_id=thread_id, role="user", content=message
# )

# == Run the Assistant
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assis_id,
    instructions="Please address the user as Bruce",
)

def wait_for_run_completion(client, thread_id, run_id, sleep_interval=3):
    """
    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[0]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)


# Run it
wait_for_run_completion(client=client, 
                        thread_id=thread_id, 
                        run_id=run.id)

# Check the run steps LOGS
run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
print(f"Run Steps --> {run_steps.data[0]}")