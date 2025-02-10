$(document).ready(function() {
    $("#chat-form").on("submit", function(e) {
        e.preventDefault();
        const loadingCircle = $("#loading-circle");
        loadingCircle.removeClass("hidden");

        const userQuestion = $("#chat-input").val().trim();
        if (userQuestion === "") {
            loadingCircle.addClass("hidden");
            return;
        }

        $("#chat-box").append(`
            <div class='message user-message'>
                <strong>Tú:</strong> ${userQuestion}
            </div>
        `);
        $("#chat-input").val("");

        $.ajax({
            type: "POST",
            url: "/ask",
            contentType: "application/json",
            data: JSON.stringify({ question: userQuestion }),
            success: function(response) {
                loadingCircle.addClass("hidden");
                if (response.answer) {
                    $("#chat-box").append(`
                        <div class='message bot-message'>
                            <div class='markdown'><strong>SERYI:</strong><br>${response.answer}</div>
                        </div>
                    `);
                } else {
                    $("#chat-box").append("<div class='message bot-message text-red-500'>Error en la respuesta</div>");
                }
                $("#chat-box").scrollTop($("#chat-box")[0].scrollHeight);
            },
            error: function() {
                loadingCircle.addClass("hidden");
                $("#chat-box").append("<div class='message bot-message text-red-500'>Error en AJAX</div>");
            }
        });
    });

    $("#clear-chat").on("click", function() {
        $("#chat-box").empty();
    });

    $("#upload-audio-btn").on("click", function() {
        $("#audio-upload").click();
    });

    $("#audio-upload").on("change", function() {
        const file = this.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append("audio", file);

        $("#chat-box").append(`
            <div class='message user-message'>
                <strong>Tú:</strong> Enviando audio: ${file.name}...
            </div>
        `);

        $.ajax({
            type: "POST",
            url: "/upload-audio",
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.error) {
                    $("#chat-box").append(`
                        <div class='message bot-message text-red-500'>
                            <strong>Error:</strong> ${response.error}
                        </div>
                    `);
                    return;
                }

                let markdownResponse = `<strong>Seryi:</strong> ${response.summary}`;
                $("#chat-box").append(`
                    <div class='message bot-message'>
                        <div class='markdown'>${markdownResponse}</div>
                    </div>
                `);
            },
            error: function() {
                $("#chat-box").append("<div class='message bot-message text-red-500'><strong>Error:</strong> No se pudo subir el audio.</div>");
            },
            complete: function() {
                $("#audio-upload").val("");
            }
        });
    });
});
