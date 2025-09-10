import json
import boto3

def lambda_handler(event, context):
    records = event.get('Records', [])
    if not records:
        return {
            'statusCode': 400,
            'body': json.dumps('No Records found in the event')
        }

    for record in records:
        body_str = record.get('body', '')
        if not body_str:
            print("No body found in this record")
            continue

        try:
            body = json.loads(body_str)
        except json.JSONDecodeError:
            print("Body is not valid JSON:", body_str)
            continue

        email = body.get('email')
        applicant_name = body.get('applicantName', 'Client')
        application_id = body.get('applicationId')
        application_status = body.get('applicationStatus', 'Pending')
        amount = body.get('amount', '$0')
        term = body.get('deadline', 'N/A')
        loan_type = body.get('loanType', 'N/A')

        ses_client = boto3.client('ses', region_name='us-east-1')

        status_color = "green" if application_status.lower() == "approved" else "red"

        html_content = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f5f5f5;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #ffffff;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }}
                .header {{
                    background-color: #0056d2;
                    color: white;
                    padding: 15px;
                    text-align: center;
                    font-size: 20px;
                    font-weight: bold;
                }}
                .content {{
                    padding: 20px;
                    font-size: 16px;
                    color: #333333;
                }}
                .status-box {{
                    border-left: 6px solid {status_color};
                    background-color: #f1f1f1;
                    padding: 10px;
                    margin: 20px 0;
                    font-weight: bold;
                    text-align: center;
                }}
                .footer {{
                    font-size: 12px;
                    color: #999999;
                    text-align: center;
                    padding: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">Loan Notification</div>
                <div class="content">
                    <p>Hello {applicant_name},</p>
                    <p>Your application with ID <b>{application_id}</b> has been processed.</p>

                    <div class="status-box">
                        Application status: {application_status}
                    </div>

                    <p><b>Requested amount:</b> {amount}</p>
                    <p><b>Term in months:</b> {term}</p>
                    <p><b>Loan type:</b> {loan_type}</p>

                </div>
                <div class="footer">
                    © CreditYa 2025.
                </div>
            </div>
        </body>
        </html>
        """

        ses_client.send_email(
            Source='lmorocoramos@gmail.com',
            Destination={
                'ToAddresses': [email]
            },
            Message={
                'Subject': {
                    'Data': 'Loan Request Decision'
                },
                'Body': {
                    'Html': {
                        'Data': html_content
                    }
                }
            }
        )

    return {
        'statusCode': 200,
        'body': json.dumps('Email sent')
    }
