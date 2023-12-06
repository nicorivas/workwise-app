/*
Component that corresponds to an individual instruction of a flowForm.
*/
import AbstractComponent from '../abstractComponent.js';

export default class FlowFormInstructionComponent extends AbstractComponent {
    constructor(element, flowForm=null) {
        super(element);
        this.flowForm = flowForm;
        this.state = {
            visible: false,
            currentElement: 0,
        };
        this.record = this.$element.find("#btn-start-record").length > 0;
        this.elements = [];
        this.init();
    }

    init() {
        this.createComponents();
        this.bindEvents();
        this.render();
    }

    createComponents() {
        this.elements = jQuery(".step__instruction__element")

        // Check if the element exists
        if (this.record) {
            this.startRecordButton = new ButtonComponent('#btn-start-record', false, false);
            this.startRecordIconButton = new ButtonComponent('#btn-start-record-icon', false, false);
            this.stopRecordButton = new ButtonComponent('#btn-stop-record', false, false);
            this.restartRecordButton = new ButtonComponent('#btn-restart-record', false, false);
        }
    }

    bindEvents() {
        if (this.record) {
            this.startRecordButton.bindEvent("click", this.startRecordHandler, null, this);
            this.startRecordIconButton.bindEvent("click", this.startRecordHandler, null, this);
            this.stopRecordButton.bindEvent("click", this.stopRecordHandler, null, this);
            this.restartRecordButton.bindEvent("click", this.restartRecordHandler, null, this);
        }
    }

    toggleVisibility(visibility) {
        this.setState({ visible: visibility });
    }

    render() {
        if (this.state.visible) {
            this.$element.removeClass('hidden');
        } else {
            this.$element.addClass('hidden');
        }
        // Show elements
    }

    destroy() {
        // Default behavior is no-op
    }

    loadMediaRecorder(mediaRecorder) {
        this.mediaRecorder = mediaRecorder;
    }

    startRecord(view) {

        view.mediaRecorder.ondataavailable = (e) => {
            view.audioChunks.push(e.data);
        };

        return new Promise((resolve, reject) => {
            
            view.mediaRecorder.onstop = (event) => {
                let blob = new Blob(view.audioChunks, { 'type': 'audio/ogg; codecs=opus' });
                resolve(blob);
            };

            // Handle the case where there is an error with the recording
            view.mediaRecorder.onerror = event => reject(event.error);
            view.mediaRecorder.start();      

        });

    }

    startRecordHandler(view) {
        if (!view.data.recording) {
            view.setData({"recording": true})
            view.startRecord(view).then(blob => {
                view.resetTimer(view);
                if (!view.data.restarting) {
                    view.transcribe(blob);
                }
                view.setData({"recording": false, "restarting": false})
            });
            view.startTimer(view);
        }
    }

    stopRecordHandler(view) {
        view.mediaRecorder.stop();
    }

    restartRecordHandler(view) {
        view.setData({"restarting": true})
        view.mediaRecorder.stop();
    }

    resetTimer(view) {
        clearInterval(view.timerInterval);
        view.time = view.RECORD_TIME;
        view.updateTimer(view);
    }

    updateTimer(view) {
        const minutes = Math.floor(view.time / 60);
        let seconds = view.time % 60;
        seconds = seconds < 10 ? '0' + seconds : seconds;
        view.timer.find("h3").text(`${minutes}:${seconds}`);
    }

    startTimer(view) {
        view.timerInterval = setInterval(() => {
            view.time--;
            view.updateTimer(view);
            if (view.time <= 0) {
                view.timer.find("h3").text("¡Se acabó el tiempo!");
                view.mediaRecorder.stop();
            }
        }, 1000);
    }

    /*
    transcribe(blob) {
        this.setData({"transcribing": true})
        let fd = new FormData();
        fd.append('audio', blob, 'audio.ogg');
        fd.append('csrfmiddlewaretoken', Cookies.get("csrftoken"));
        fd.append('pitch_id', this.pitchId);
        jQuery.ajax({
            type: 'POST',
            url: "/flow/transcribe/",
            data: fd,
            processData: false,
            contentType: false,
            success: (successData) => {
                this.transcriptText.text(successData.text);
                this.flowForm.nextStep();
            },
            error: (xhr, status, error) => {
                this.showError("Error en transcripción");
                this.restartRecordHandler(this);
                this.setData({"transcribing": false});
            }
        })
    }

    analyse(view) {
        view.flowForm.nextStep();
        view.setData({"analysing": true});
        view.analysisText.find(".text").text("");
        view.analysisText.find(".indicator").show();

        // Update pitch with data
        let data = jQuery("#pitch-form").serializeArray();
        let jsonData = {};
        data.forEach(function(item) {
            jsonData[item.name] = item.value;
        });
        let url = `/api/pitch/${view.pitchId}/`
        jQuery.ajax({
            type: 'PUT',
            url: url,
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: (successData) => {
                //
            },
            beforeSend: function(xhr) {
                // Include the CSRF token as a header
                xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
            },
            error: (xhr, status, error) => {
                console.error(xhr);
            },
        })

        // Long analysis (sent by email)
        url = '/flow/analyse_long/';
        data.push({"name":"pitch_id", "value":view.pitchId});
        jQuery.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: (successData) => {
                //
            },
            beforeSend: function(xhr) {
                // Include the CSRF token as a header
                xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
            },
            error: (xhr, status, error) => {
                console.error(xhr);
            },
        })

        view.llm.stream("/flow/analyse/", "id_pitch", "step__body__answer", {"pitch_id": view.pitchId}).then((response) => {
            let data = jQuery("#pitch-form").serializeArray();
            let jsonData = {};
            // Check if length of response is long enough to be a proper answer
            data.forEach(function(item) {
                jsonData[item.name] = item.value;
            });
            jsonData["pitch_analysis_short"] = response;
            url = `/api/pitch/${view.pitchId}/`
            jQuery.ajax({
                type: 'PUT',
                url: url,
                contentType: 'application/json',
                data: JSON.stringify(jsonData),
                success: (successData) => {
                    //
                },
                beforeSend: function(xhr) {
                    // Include the CSRF token as a header
                    xhr.setRequestHeader("X-CSRFToken", Cookies.get("csrftoken"));
                },
                error: (xhr, status, error) => {
                    console.error(xhr);
                },
            })
            view.setData({"analysing": false});
            // Analizar button
            this.setState({"status": "idle"})
        }).catch((error) => {
            view.setData({"analysing": false});
            // Analizar button
            this.setState({"status": "idle"})
        })
    }

    uploadAudio(blob) {
        let fd = new FormData();
        fd.append('audio', blob, 'audio.ogg');
        fd.append('csrfmiddlewaretoken', Cookies.get("csrftoken"));
        jQuery.ajax({
            type: 'POST',
            url: '/flow/transcribe/',
            data: fd,
            processData: false,
            contentType: false,
            success: (successData) => {
                //
            },
            error: (xhr, status, error) => {
                console.error(xhr);
            },
        });
    }
    */

}