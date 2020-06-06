import cuid, sys, os
from dotenv import load_dotenv
from notifications_python_client.notifications import NotificationsAPIClient

# Load .env
load_dotenv()

# Set up a new Notify client 
notifications_client = NotificationsAPIClient(os.getenv("NOTIFY_KEY"))

# Generate a unique reference 
id_gen = cuid.CuidGenerator()
id = id_gen.cuid()

# Get the file redirected to stdin (as a binary file)
input = sys.stdin.buffer.read()
with open(id, "wb") as output:
   output.write(input)

# Convert from PostScript to PDF (has the effect of stripping out PCL which Notify doesn't like)
os.system("ps2pdf {} {}.pdf".format(id, id))

# Try to send a letter
with open("{}.pdf".format(id), "rb") as file_to_send:
    notification = notifications_client.send_precompiled_letter_notification(
        reference=id, pdf_file=file_to_send
    )
    print(notification)

# Delete local files 
os.remove(id)
os.remove("{}.pdf".format(id))