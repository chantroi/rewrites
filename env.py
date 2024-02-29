import os.getenv as ENV

secret = ENV("SECRET")
mq_host = ENV("MQ_HOST")
mq_user = ENV("MQ_USER")
mq_pw = ENV("MQ_PW")
mq_vhost = ENV("MQ_VHOST")