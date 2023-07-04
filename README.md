# bing

A simple example using acheong08's EdgeGPT

## How to use

1. build image
   ```shell
   docker image build -t cphovo/bing .
   ```

2. start service
   ```shell
   docker run -it -p 8000:8000 cphovo/bing
   ```

3. send request
   ```shell
   curl -X POST -H "Authorization: cphovo-e1fecb424bb92b04223f5bc7ebe938d94" -H "Content-Type: application/json" -d '{
     "text": "hello",
     "style": "creative"
   }' http://your_ip:8000/bing/ask
   ```

4. response
   ```json
   {
       "text":"Hello, this is Bing. How can I help? 😊",
       "author":"bot","sources":"Hello, this is Bing. How can I help? 😊\n",
       "sources_text":"Hello, this is Bing. How can I help? 😊\n",
       "suggestions":[
            "What is the weather like in Adelaide?",
            "Tell me a joke.",
            "Who won the last Australian Open?"
        ],
        "messages_left":9,
        "max_messages":10,
        "adaptive_text":"Hello, this is Bing. How can I help? 😊\n"
    }                                                                                   
   ```

Note: Use `proxychains` to solve websocket error problems through proxies.

## Thanks

This demo reference [acheong08](https://github.com/acheong08/EdgeGPT)'s open source project, many thanks 🙏.