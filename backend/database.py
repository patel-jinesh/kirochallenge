import boto3
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid
from botocore.exceptions import ClientError


class DynamoDBClient:
    def __init__(self):
        self.table_name = os.getenv("DYNAMODB_TABLE_NAME", "EventsTable")
        
        # Initialize DynamoDB client
        if os.getenv("AWS_ENDPOINT_URL"):
            # For local development with DynamoDB Local
            self.dynamodb = boto3.resource(
                'dynamodb',
                endpoint_url=os.getenv("AWS_ENDPOINT_URL")
            )
        else:
            self.dynamodb = boto3.resource('dynamodb')
        
        self.table = self.dynamodb.Table(self.table_name)

    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new event in DynamoDB"""
        # Use provided eventId or generate new one
        event_id = event_data.pop('eventId', None) or str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        item = {
            'eventId': event_id,
            'createdAt': timestamp,
            'updatedAt': timestamp,
            **event_data
        }
        
        try:
            self.table.put_item(Item=item)
            return item
        except ClientError as e:
            raise Exception(f"Error creating event: {e.response['Error']['Message']}")

    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get an event by ID"""
        try:
            response = self.table.get_item(Key={'eventId': event_id})
            return response.get('Item')
        except ClientError as e:
            raise Exception(f"Error getting event: {e.response['Error']['Message']}")

    def list_events(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all events, optionally filtered by status"""
        try:
            if status_filter:
                response = self.table.scan(
                    FilterExpression='#status = :status',
                    ExpressionAttributeNames={'#status': 'status'},
                    ExpressionAttributeValues={':status': status_filter}
                )
            else:
                response = self.table.scan()
            return response.get('Items', [])
        except ClientError as e:
            raise Exception(f"Error listing events: {e.response['Error']['Message']}")

    def update_event(self, event_id: str, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update an event"""
        if not update_data:
            return self.get_event(event_id)
        
        # Build update expression
        update_expression = "SET updatedAt = :updatedAt"
        expression_values = {':updatedAt': datetime.utcnow().isoformat()}
        expression_names = {}
        
        # DynamoDB reserved keywords that need attribute name placeholders
        reserved_keywords = ['status', 'date', 'location', 'capacity', 'title', 'description', 'organizer']
        
        for key, value in update_data.items():
            if value is not None:
                placeholder = f":{key}"
                # Always use attribute name placeholders for safety
                if key in reserved_keywords:
                    attr_name = f"#{key}"
                    expression_names[attr_name] = key
                    update_expression += f", {attr_name} = {placeholder}"
                else:
                    update_expression += f", {key} = {placeholder}"
                expression_values[placeholder] = value
        
        try:
            kwargs = {
                'Key': {'eventId': event_id},
                'UpdateExpression': update_expression,
                'ExpressionAttributeValues': expression_values,
                'ReturnValues': 'ALL_NEW'
            }
            
            if expression_names:
                kwargs['ExpressionAttributeNames'] = expression_names
            
            response = self.table.update_item(**kwargs)
            return response.get('Attributes')
        except ClientError as e:
            raise Exception(f"Error updating event: {e.response['Error']['Message']}")

    def delete_event(self, event_id: str) -> bool:
        """Delete an event"""
        try:
            self.table.delete_item(Key={'eventId': event_id})
            return True
        except ClientError as e:
            raise Exception(f"Error deleting event: {e.response['Error']['Message']}")


# Singleton instance
db_client = DynamoDBClient()
