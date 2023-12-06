import AbstractView from '../abstractView.js';
import FlowFormComponent from '../../components/flowFormComponent/flowForm.js';
import ButtonComponent from '../../components/buttonComponent/button.js';
import LLM from '../../js/llm.js';

export default class FlowView extends AbstractView {
    
    constructor(element, view, id=null) {
        super(element);
        this.RECORD_TIME = 4 * 60;
        this.flowForm;
        this.pitchId = this.$element.data("id");
        this.submitStepOne = null;
        this.data = {
            "recording": false,
            "transcribing": false,
        }
        this.time = this.RECORD_TIME;
        this.timer = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.llm = new LLM();
        this.blob = null;
        this.transcriptText = jQuery("#id_pitch");
        this.analysisText = jQuery(".step__body__answer");
        this.init();
    }

    init() {
        this.load();
    }

    load() {
        this.loadComponents();
        if (this.pitchId) {
            jQuery.ajax({
                type: 'GET',
                url: `/api/pitch/${this.pitchId}`,
                success: (pitch) => {
                    const md = markdownit();
                    let result = md.render(pitch.pitch_analysis_short);
                    this.analysisText.find(".text").html(result);
                },
                error: (xhr, status, error) => {
                    // Handle AJAX errors
                    console.error(xhr);
                }
            })
        }


        this.setData(this.data);
    }

    loadComponents() {
        this.timer = jQuery('#timer');

        this.flowForm = new FlowFormComponent('#flow-container');
        this.flowForm.init();

        this.navPrevButton = new ButtonComponent('#btn-prev', true, false);
        this.navNextButton = new ButtonComponent('#btn-next', true, false);

        this.createPitchButton = new ButtonComponent('#btn-create-pitch', true, false);
        this.startRecordButton = new ButtonComponent('#btn-start-record', false, false);
        this.startRecordIconButton = new ButtonComponent('#btn-start-record-icon', false, false);
        this.stopRecordButton = new ButtonComponent('#btn-stop-record', false, false);
        this.restartRecordButton = new ButtonComponent('#btn-restart-record', false, false);
        this.analyseButton = new ButtonComponent('#btn-analyse', true, false);
        this.lastButton = new ButtonComponent('#btn-last', false, false);
        this.finishButton = new ButtonComponent('#btn-finish', true, false);

        this.bindEvents();
    }

    bindEvents() {
        this.navPrevButton.bindEvent('click', this.flowForm.prevStep, null, this.flowForm);
        this.navNextButton.bindEvent('click', this.flowForm.nextStep, null, this.flowForm);
        this.createPitchButton.bindEvent('click', this.createPitchHandler, null, this);
        this.startRecordButton.bindEvent("click", this.startRecordHandler, null, this);
        this.startRecordIconButton.bindEvent("click", this.startRecordHandler, null, this);
        this.stopRecordButton.bindEvent("click", this.stopRecordHandler, null, this);
        this.restartRecordButton.bindEvent("click", this.restartRecordHandler, null, this);
        this.analyseButton.bindEvent("click", this.analyse, null, this);
        this.lastButton.bindEvent("click", this.last, null, this);
        this.finishButton.bindEvent("click", this.finish, null, this);
    }

    /* Functions */

    createPitchHandler(view) {
        view.createPitch(this);
    }

    createPitch(button) {
        let data = jQuery("#pitch-form").serializeArray();
        data.push({name: "csrfmiddlewaretoken", value: Cookies.get("csrftoken")});
        let url = "/api/pitch/" ;
        jQuery.ajax({
            type: 'POST',
            url: url,
            data: data,
            success: (successData) => {
                this.pitchId = successData.pk;
                this.flowForm.nextStep();
                button.setState({"status":"idle"})
                // Change url
                window.history.pushState("", "", `/flow/carozzi/${this.pitchId}/`);
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                for (let field in xhr.responseJSON) {
                    let elementId = `#id_${field}`
                    let elementErrorId = `#id_${field}-error`                    
                    jQuery(elementId).addClass("is-invalid")
                    if ("This field may not be blank." == xhr.responseJSON[field]) {
                        jQuery(elementErrorId).find("p").text("Este campo no puede estar en blanco.");
                    } else if ("Enter a valid email address." == xhr.responseJSON[field]) {
                        jQuery(elementErrorId).find("p").text("Por favor ingresa un correo válido.");
                    } else {
                        jQuery(elementErrorId).find("p").text(xhr.responseJSON[field]);
                    }
                    button.setState({ "status": "idle" })
                }
            }
        })
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
        jQuery.ajax({
            type: 'POST',
            url: '/flow/analyse_long/',
            contentType: 'application/json',
            data: JSON.stringify(jsonData),
            success: (successData) => {
                //
                console.log(successData);
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
            data.forEach(function(item) {
                jsonData[item.name] = item.value;
            });
            jsonData["pitch_analysis_short"] = response;
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
            console.error("Error while streaming", error);
            view.setData({"analysing": false});
            // Analizar button
            this.setState({"status": "idle"})
        })
    }
    */

    last(view) {
        view.flowForm.nextStep();
    }

    finish() {
        window.location.href = "/flow/carozzi/";
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
                /* */
            },
            error: (xhr, status, error) => {
                console.error(xhr);
            },
        });
    }

    render() {
        if (this.data.recording) {
            jQuery(".record-icon").addClass("record-icon--recording");
            jQuery(".record-icon").find(".pulse").show();
            this.startRecordButton.$element.hide();
            this.stopRecordButton.$element.show();
            this.restartRecordButton.$element.show();
        } else {
            jQuery(".record-icon").removeClass("record-icon--recording");
            jQuery(".record-icon").find(".pulse").hide();
            this.startRecordButton.$element.show();
            this.stopRecordButton.$element.hide();
            this.restartRecordButton.$element.hide();
        }
        if (this.data.transcribing) {
            jQuery("#step__record").hide();
            jQuery("#step__transcribe").show();
        } else {
            jQuery("#step__record").show();
            jQuery("#step__transcribe").hide();
        }
        if (this.data.analysing) {
            jQuery("#step__body__answer__indicator").show();
        } else {
            jQuery("#step__body__answer__indicator").hide();
        }
    }

}