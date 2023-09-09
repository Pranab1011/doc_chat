$(document).ready(function() {

    $("#send-button").click(function () {
        sendMessage();
    });

    $("#user-message").keypress(function (e) {
        if (e.which === 13) {
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = $("#user-message").val();
        if (userMessage.trim() !== "") {
            // Create a new message element
            const messageElement = $("<div class='message user-message'></div>");
            messageElement.text(userMessage);

            // Append it to the chat messages
            $("#chat-messages").append(messageElement);

            // Clear the input field
            $("#user-message").val("");

            // Scroll to the bottom of the chat container
            $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);

            $.ajax({
                type: "POST",
                url: "/message",
                data: { message: userMessage },
                success: function(response) {
                    const reply = response.reply;
                    const replyElement = $("<div class='message server-response'></div>");
                    replyElement.text(reply);
                    $("#chat-messages").append(replyElement);
                    $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
                }
            });
        }
    }

    const processButton = document.getElementById("processbutton");
    const dropContainer = document.getElementById("dropcontainer");
    const uploadButton = document.getElementById("processbutton");


    dropContainer.addEventListener("dragover", (e) => {
    // prevent default to allow drop
    e.preventDefault()
    }, false);

    dropContainer.addEventListener("dragenter", () => {
    dropContainer.classList.add("drag-active")
    });

    dropContainer.addEventListener("dragleave", () => {
    dropContainer.classList.remove("drag-active")
    });

    dropContainer.addEventListener("drop", (e) => {
    e.preventDefault()
    dropContainer.classList.remove("drag-active")
    fileInput.files = e.dataTransfer.files
    });


    $("#processbutton").click(function() {
        const fileInput = document.getElementById("files");
        console.log(fileInput.files.length);

        if (fileInput.files.length > 0) {
            const selectedFile = fileInput.files[0];
            // Create a FormData object to send the file
            var formData = new FormData();
            formData.append("file", selectedFile);

            $.ajax({
                type: "POST",
                url: "/upload",
                data: formData,
                contentType: false,
                processData: false,
                success: function(response) {
                    // Send a follow-up message to the chat box
                    const followUpMessage = response.follow_up_message;
                    const replyElement = $("<div class='message server-response'></div>");
                    replyElement.text(followUpMessage);
                    $("#chat-messages").append(replyElement);
                    $("#chat-messages").scrollTop($("#chat-messages")[0].scrollHeight);
                }
            });
        }
    });
});