export default class LLM {

    constructor() {
        /* */
    }


    stream(view_url, source_element_id, destination_element_id, view_data=null) {

        //console.log("LLM:stream");

        return new Promise((resolve, reject) => {
        
            /*
            This function is used to stream LLM responses from the server to the client.
            It opens a websocket connection to the server.
            Then it sends an AJAX request to the server, with data from source_element_id.
            The data is taken from the source element's val() value.
            The server then sends a response with a chunk of data to the client via the websocket connection.
            The response is used to render the destination_element_id.
            TODO: Don't assume that response is markdown.
            */

            let csrf_token = Cookies.get('csrftoken');
            let response = "";
            // Parameter sets the group of the socket connection to the url.
            // This allows us to have multiple socket connections open at once, and stream answers
            // from the server to specific ones based on the url that called the view.
            const hostname = window.location.hostname
            let websocket_url = ""
            // If its localhost
            if (hostname == "127.0.0.1" || hostname == "localhost") {
                websocket_url = `ws://${hostname}:8000/ws/openai_stream/?group_name=` + view_url
            } else {
                websocket_url = `wss://${hostname}/ws/openai_stream/?group_name=` + view_url
            }
            //console.log("Connecting to ", websocket_url);
            const socket = new WebSocket(websocket_url);

            // Check if source element exists
            if (jQuery(`#${source_element_id}`).length == 0) {
                //console.log(`LLM:stream: source_element_id ${source_element_id} does not exist`);
                return;
            }

            // Check if destination element exists with jQuery
            if (jQuery(`#${destination_element_id}`).length == 0) {
                //console.log(`LLM:stream: destination_element_id ${destination_element_id} does not exist`);
                return;
            }

            socket.onopen = function (event) {
                // Called when the socket connection is established.
                // AJAX call to the view
                //console.log("LLM:stream.socket.onopen")
                let data = {
                    csrfmiddlewaretoken: csrf_token,
                    query: jQuery(`#${source_element_id}`).val(),
                };
                data = { ...data, ...view_data };
                jQuery.ajax({
                    url: view_url,
                    type: "POST",
                    data: data,
                    success: function (data) {
                        // Nothing to do: call is made from the server to the socket directly.
                    },
                    error: function (xhr, errmsg, err) {
                        //console.log(`streamCallGeneral.error:\n ${xhr.status}: ${xhr.responseText}`);
                    }
                });
            };

            socket.onmessage = function (event) {
                // Each message is a response from the server with a chunk of the model response.
                // We save the total response and each time we get a new chunk we render the markdown.
                //console.log("LLM:stream.socket.onmessage");
                const data = JSON.parse(event.data);
                if (data.status == "continue") {
                    // Add received chunk, in data.response, to total response
                    // Update the destination DOM element with the response
                    response = data.response_text;
                    const md = markdownit();
                    let result = md.render(data.response_text);
                    jQuery(`#${destination_element_id}`).find(".indicator").hide();
                    jQuery(`#${destination_element_id}`).find(".text").html(result);
                } else if (data.status == "end") {
                    response = data.response_text;
                    const md = markdownit();
                    let result = md.render(data.response_text);
                    jQuery(`#${destination_element_id}`).find(".text").html(result);
                    socket.close();
                };
            };

            socket.onerror = function (error) {
                //console.log(`LLM:stream.socket.onerror: ${error.message}`);
            };

            socket.onclose = (event) => {
                //console.log("LLM:stream.socket.onclose", event)
                if (event.wasClean) {
                    //console.log(`Connection closed cleanly, code=${event.code}, reason=${event.reason}`);
                    resolve(response);
                } else {
                    //console.error('Connection died', event);
                    reject();
                }
            }
        });
    }
}