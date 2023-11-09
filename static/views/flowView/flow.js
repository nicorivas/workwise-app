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
        this.transcriptText = jQuery(".step__body__text");
        this.analysisText = jQuery(".step__body__answer");
        this.init();
    }

    init() {
        console.log("ProjectView.init()", this.parentView);
        this.load();
    }

    load() {
        console.log("ProjectView.load()");

        this.loadComponents();
        this.setData(this.data);
    }

    loadComponents() {
        console.log("ProjectView.loadComponents()");

        this.timer = jQuery('#timer');

        this.flowForm = new FlowFormComponent('#flow-container');
        this.flowForm.init();

        this.createPitchButton = new ButtonComponent('#btn-create-pitch', true, false);
        this.startRecordButton = new ButtonComponent('#btn-start-record', false, false);
        this.startRecordIconButton = new ButtonComponent('#btn-start-record-icon', false, false);
        this.stopRecordButton = new ButtonComponent('#btn-stop-record', false, false);
        this.restartRecordButton = new ButtonComponent('#btn-restart-record', false, false);
        this.analyseButton = new ButtonComponent('#btn-analyse', true, false);
        this.finishButton = new ButtonComponent('#btn-finish', true, false);

        this.bindEvents();
    }

    bindEvents() {
        console.log("ProjectView.bindEvents");

        this.createPitchButton.bindEvent('click', this.createPitchHandler, null, this);
        this.startRecordButton.bindEvent("click", this.startRecordHandler, null, this);
        this.startRecordIconButton.bindEvent("click", this.startRecordHandler, null, this);
        this.stopRecordButton.bindEvent("click", this.stopRecordHandler, null, this);
        this.restartRecordButton.bindEvent("click", this.restartRecordHandler, null, this);
        this.analyseButton.bindEvent("click", this.analyse, null, this);
        this.finishButton.bindEvent("click", this.finish, null, this);
    }

    createPitchHandler(view) {
        view.createPitch(this);
    }

    createPitch(button) {
        let data = jQuery("#create-pitch-form").serializeArray();
        console.log(Cookies.get("csrftoken"));
        data.push({name: "csrfmiddlewaretoken", value: Cookies.get("csrftoken")});
        console.log(data);
        jQuery.ajax({
            type: 'POST',
            url: "/api/pitch/",
            data: data,
            success: (successData) => {
                console.log(successData);
                this.pitchId = successData.pk;
                this.flowForm.nextStep();
                button.setState({ "status": "idle" })
            },
            error: (xhr, status, error) => {
                // Handle AJAX errors
                for (let field in xhr.responseJSON) {
                    console.log(xhr);
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
        console.log(this);

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
        console.log("startRecordHandler");
        if (!view.data.recording) {
            view.setData({"recording": true})
            view.startRecord(view).then(blob => {
                console.log(blob);
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
        console.log("stopRecordHandler");
        view.mediaRecorder.stop();
    }

    restartRecordHandler(view) {
        console.log("restartRecord");
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

    transcribe(blob) {
        console.log("transcribe", blob);
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
                console.log("Transcription", successData.text);
                this.transcriptText.text(successData.text);
                this.flowForm.nextStep();
            },
            error: (xhr, status, error) => {
                this.showError("Error en transcripción");
                this.restartRecord(this);
                this.setData({"transcribing": false});
            }
        })
    }

    analyse(view) {
        view.flowForm.nextStep();
        view.setData({"analysing": true});
        view.analysisText.find(".text").text("");
        view.analysisText.find(".indicator").show();
        view.llm.stream("/flow/analyse/", "step__body__text", "step__body__answer", {"pitch_id": view.pitchId}).then(() => {
            view.setData({"analysing": false});
        });
    }

    finish() {
        window.location.href = "/flow/carozzi/";
    }

    uploadAudio(blob) {
        console.log("uploadAudio");
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
                console.log(successData)
            },
            error: (xhr, status, error) => {
                console.log(xhr);
                console.log(status);
                console.log(error);
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