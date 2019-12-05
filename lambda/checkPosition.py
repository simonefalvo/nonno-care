import os
import boto3
import math


def handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    sns = None
    batch_size = len(event['Records'])
    for record in event['Records']:
        attributes = record["messageAttributes"]
        sensor_id = attributes["sensor_id"]["stringValue"]
        timestamp = attributes["timestamp"]["stringValue"]
        latitude = float(attributes["latitude"]["stringValue"])
        longitude = float(attributes["longitude"]["stringValue"])
        heart_rate = int(attributes["heart_rate"]["stringValue"])

        # retrieve user safety zone info
        table = dynamodb.Table(os.environ['USER_DATA_TABLE'])

        response = table.get_item(
            Key={
                'sensor_id': sensor_id
            }
        )
        item = response['Item']
        #print("Item:\n", item)

        safety_lat = float(item['safety_latitude'])
        safety_long = float(item['safety_longitude'])
        safety_radius = float(item['safety_radius'])

        # check if current position is inside the safety zone
        if distance(safety_lat, safety_long, latitude, longitude) > safety_radius:
            #print("WARNING: Outside the safety zone!")
            if sns is None:
                # Create an SNS client
                sns = boto3.client('sns')

            # Publish a simple message to the specified SNS topic
            sns.publish(
                TopicArn=os.environ['SNS_TOPIC_NOTIFY'],
                Message='Attenzione: fuoriuscita dalla zona di sicurezza',
                MessageAttributes={
                    'sensor_id': {
                        'DataType': 'Number',
                        'StringValue': sensor_id
                    },
                    'timestamp': {
                        'DataType': 'String',
                        'StringValue': timestamp
                    },
                    'type': {
                        'DataType': 'String',
                        'StringValue': 'Safety zone'
                    },
                    'latitude': {
                        'DataType': 'Number.float',
                        'StringValue': str(latitude)
                    },
                    'longitude': {
                        'DataType': 'Number.float',
                        'StringValue': str(longitude)
                    },
                    'heart_rate': {
                        'DataType': 'Number',
                        'StringValue': str(heart_rate)
                    }
                }
            )
        else:
            #print("Dentro la safety zone")
            print("JOB_ID {}, RequestId: {}, BatchSize: {}"
                  .format(sensor_id + timestamp.replace('.', '-'), context.aws_request_id, batch_size))


# da posizione in gradi decimali a gradi, primi, sec (41.85577° = 41 ° 51 ' 20 ")
def convert_dec_to_grad(grad):
    d = int(grad)
    m = int((grad - d) * 60)
    s = int((grad - d - m / 60) * 3600)

    return d, m, s


# da posizione in gradi primi secondi a decimali (41 ° 51 ' 20" = 41.85555)
def convert_grad_to_dec(d, m, s):
    rad = d + (m / 60) + (s / 3600)
    return rad


# da posizione in decimali a posizione in radianti (41.85555 = 0.73051725)
def convert_dec_to_rad(decimal):
    return math.radians(decimal)


# da posizione in radianti a posizione in decimali (0.73051725 = 41.85555)
def convert_rad_to_dec(rad):
    return math.degrees(rad)


def distance(lat_a, long_a, lat_b, long_b):
    """
    uses the ‘haversine’ formula to calculate the great-circle distance between two points –
        that is, the shortest distance over the earth’s surface
    a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    c = 2 ⋅ atan2( √a, √(1−a) )
    d = R ⋅ c
        where	φ is latitude, λ is longitude, R is earth’s radius (mean radius = 6,371km);
        note that angles need to be in radians to pass to trig functions!
    :return: the distance in kilometers between two points
    """

    r = 6371  # kilometers
    phi1 = convert_dec_to_rad(lat_a)
    phi2 = convert_dec_to_rad(lat_b)
    delta_phi = convert_dec_to_rad(lat_b - lat_a)
    delta_lambda = convert_dec_to_rad(long_b - long_a)

    a = math.sin(delta_phi / 2) * math.sin(delta_phi / 2) + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) * math.sin(delta_lambda / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c
