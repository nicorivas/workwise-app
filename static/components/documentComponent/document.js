import AbstractComponent from '../abstractComponent.js';
import SelectorComponent from '../selectorComponent/selector.js';
import KebabComponent from '../kebabComponent/kebab.js';

export default class DocumentComponent extends AbstractComponent {

    constructor(element, task) {
        super(element);
        // Elements
        this.$header = this.$element.find(".document__header");
        this.$headerFormats = this.$element.find(".document__header__formats");
        this.$headerFormatClose = this.$element.find(".document__header__format-close");
        this.$headerToolbar = this.$element.find(".document__header__toolbar");
        this.$headerStreaming = this.$element.find(".document__header__streaming");
        this.$headerLoading = this.$element.find(".document__header__loading");
        this.$body = this.$element.find(".document__body");
        // Define state
        this.state = {
            "id": this.$element.data("id"),
            "status": "idle",
            "name": null,
            "format_open": this.$element.hasClass("document--format")
        }
        // Others
        this.reply;
        this.editorJS = false;
        this.editor;
        this.editorData;
        this.task = task;
        this.sections = [];
        this.selectorFormats;     
        this.kebabFormats;   
        this.init(element, task);
    }

    init() {
        // Formats Kebab
        if (this.$header.length != 0) {
            this.kebabFormats = new KebabComponent(this.$headerFormats.find("#document-formats-kebab"));
            this.getFormats().then((formats) => {;
                for (const format of formats) {
                    let $item = this.kebabFormats.addItem(format.name, format.id);
                    $item.on("click", (e) => { 
                        console.log(format.id);    
                        this.setState({
                            "status":"loading",
                            "id": format.id,
                            "format_open": true
                        });
                        this.editorLoad();
                    })
                }
            })
        }

        // Formats selector
        /*
        this.selectorFormats = new SelectorComponent("#selector-formats");
        this.selectorFormats.itemClicked = (item) => {
            console.log("DocumentComponent.selectorFormats.itemClicked()", item);

            this.setState({
                "id": this.$element.data("id"),
                "name": item.find(".selector-item-text").text(),
                    
            })
            this.name = item.find(".selector-item-text").text();
            this.openFormat();
            if (this.task) {
                // Select format instruction.
                // Only way to select it is by name, as we don't know the relation document_id - instruction_id
                this.task.selectFormatInstruction(this.name);
            }    
        }
        */

        // Formats close
        jQuery(".document__header__format-close").click(() => {
            console.log("Close format");
            this.setState({
                "status":"loading",
            });
            this.closeFormat();
        })

        // Save
        this.$element.find("#document__header__toolbar__save").click(() => {
            this.save(this.state["id"]);
        })

        // Load the editor.
        if (this.state.id) {
            this.editorLoad();
        }

        this.setState(this.state);

    }

    getFormats() {
        return new Promise((resolve, reject) => { 
            jQuery.ajax({
                url: `/api/document/`,
                type: 'GET',
                data: {"is_format": true, "parent_document_id": this.state["id"]},
                success: (data) => {
                    resolve(data);
                },
                error: (jqXHR, textStatus, errorThrown) => {
                    reject();
                }
            
            })
        })
    }

    openFormatByName(format_name) {
        let formatId = this.kebabFormats.$element.find(`.kebab__menu__item__text:contains("${format_name}")`).closest(".kebab__menu__item").attr("id");
        if (!formatId) {
            return;
        } else {
            this.name = format_name;
            this.setState({
                "id": formatId,
            });
            this.openFormat();
        }
    }

    openFormat() {
        if (this.state["format_open"]) return;

        this.setState({"format_open": true});

        // Read document
        this.editorRead();
    }

    closeFormat() {
        if (!this.state["format_open"]) return;

        // Set state
        this.setState({
            "format_open":false,
            "id":this.$element.data("id")
        });

        this.editorRead();

        if (this.task) {
            this.showToolbar();
            this.task.deselectFormatInstruction(this.name);
        }

        // Open parent document
        /*
        let format_name = this.name;
        
        this.name = null;
        
        
        // Change document looks
        this.$element.removeClass("document-format");
        this.$element.find(".document-header").removeClass("document-header-format")
        if (this.task) {
            this.showToolbar();
            this.$element.find(".document-format-close-button").hide();
            this.task.deselectFormatInstruction(format_name);
            this.selectorFormats.clear();
        }
        */
    }

    getId() {
        return this.$element.data("id");
    }

    bindEvents() {
        console.log("DocumentComponent.bindEvents");
    }

    hideToolbar() {
        this.$element.find(".document-toolbar").hide();
    }

    showToolbar() {
        this.$element.find(".document-toolbar").show();
    }

    elementUpdate(data) {
        jQuery("#project-document-wrapper").html(data);
        this.$element = jQuery(".document");

    }

    read(document_id=null) {
        console.log("DocumentComponent.read", document_id, this.state["id"]);

        // Set state to loading.
        this.setState({
            "status": "loading",
            "id": document_id ?? this.state["id"]
        });

        // Reset editor
        this.editorLoad();

        let url = `/document/${this.state["id"]}/`
        // Call document:read
        return new Promise((resolve, reject) => { 
            jQuery.ajax({
                url: url,
                type: "GET",
                success: (data) => {
                    // Replace wrapper with document data
                    console.log(data);
                    //this.elementUpdate(data)
                },
                error: function (xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText);
                    reject(err);
                },
                complete: () => {
                    if (jQuery(".document").hasClass("document--format")) {
                        this.openFormat();
                    }
                    this.setState({"status": "idle"});
                    resolve();
                }
            });
        });
    }

    editorLoad() {
        this.$element.find("#document-editor").html("");
        if (this.editorJS) {
            this.editor = new EditorJS({
                holder: 'document-editor',
                tools: {
                    header: Header,
                    delimiter: Delimiter,
                    paragraph: {
                        class: Paragraph,
                        inlineToolbar: true,
                    },
                    list: {
                        class: List,
                        inlineToolbar: true,
                        config: {
                            defaultStyle: 'unordered'
                        }
                    }
                },
                onReady: () => {
                    console.log('Editor.js is ready to work!')
                    this.editorRead();
                }
            });
        } else {
            this.editorRead();
        };
    }

    editorRead() {
        jQuery("#document-editor-wrapper-indicator").show();
        jQuery("#document-editor-wrapper").hide();
        jQuery.ajax({
            url: `/document/api/v1/document/${this.state["id"]}/reply`,
            type: 'GET',
            success: (data) => {
                jQuery("#document-editor-wrapper-indicator").hide();
                jQuery("#document-editor-wrapper").show();
                console.log(data);
                // Update if data is not empty
                if (!jQuery.isEmptyObject(data)) {
                    this.setState({"status":"idle"});
                    if (this.editorJS) {
                        this.editorData = data;
                        this.editorUpdate();
                        if (this.task) {
                            //this.task.documentReady();
                        }
                    } else {
                        if (data.reply) {
                            this.reply = data.reply;
                            let md = markdownit();
                            let html = md.render(this.reply);
                            jQuery("#document-editor").html(html);
                        } else {
                            jQuery("#document-editor").html("");
                        }
                        
                    }
                }
            }
        })
    }

    editorClear() {
        if (this.editorJS) {
            console.log("DocumentComponent.editorClear");
            if (this.editor) {
                this.editor.clear();
            } else {
                console.warn("DocumentComponent.editorClear: editor not found")
            }
        } else {
            this.$element.find("#document-editor").html("");
        }
    }

    editorUpdate(save = false) {
        if (this.editorJS) {
            this.editor.clear().then(() => {
                this.editor.render(this.editorData).then(() => {
                    this.editor.save().then((output_data) => {
                        this.editorData = output_data;
                        this.loadSections();
                        if (save) {
                            this.save_back(this.state["id"], output_data)
                        }
                    }).catch((error) => {
                        console.log('# Saving document failed: ', error)
                    });
                });
            })
        } else {
            let md = markdownit();
            let result = md.render(this.reply);
            jQuery("#document-editor").html(result);
            if (save) {
                this.save_back(this.state["id"], this.reply, false)
            }
        }
    }

    stream(instruction, instruction_element_id) {

        console.log("DocumentComponent:stream", instruction, instruction_element_id);

        let document_id = this.$element.data("id");
        let socket_data = {};
        let response = "";
        let get_prompt_data = {};
        let instruction_element_call_url = `/instruction/${instruction.id}/element/${instruction_element_id}/call_prompt`;

        const hostname = window.location.hostname;
        let websocket_url = "";
        // If its localhost
        if (hostname == "127.0.0.1" || hostname == "localhost") {
            websocket_url = `ws://${hostname}:8000/ws/openai_stream/?group_name=` + instruction_element_call_url;
        } else {
            websocket_url = `ws://${hostname}:80/ws/openai_stream/?group_name=` + instruction_element_call_url;
        }
        const socket = new WebSocket(websocket_url);
    
        this.setState({
            "status": "streaming"
        })
        // Reset editor
        this.editorClear();

        // Here we get the data of the instruction 'form'
        // This is the data that is stored in the instruction, that is, it's state.
        // We get the data by class: every element that has .instruction-input is part of the data.
        jQuery(`#instruction_${instruction.id}`).find(".instruction-input").each(function () {
            // Not elements have a value (as inputs, textfields), as we sometimes store data in other html elements.
            if (jQuery(this).val()) {
                get_prompt_data[jQuery(this).attr("name")] = jQuery(this).val();
            } else {
                get_prompt_data[jQuery(this).attr("name")] = jQuery(this).attr("value")
            }
        });
    
        // Call to inititate stream. Get the prompt and then call the LLM.
        jQuery.ajax({
            url: instruction_element_call_url,
            type: "POST",
            data: get_prompt_data,
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            },
            success: function (data) {
                socket_data = data;
            },
            error: function (xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
                response = "";
            }
        });
    
        let time_last_message = 0;
    
        socket.onmessage = (event) => {
            // Each message is a response from the server with a chunk of the model response.
            // We save the total response and each time we get a new chunk we render the markdown.
            const data = JSON.parse(event.data);
            if (data.status == "continue") {
                response += data.response;
                // Calculate ellapsed time since last message
                let time_since_last_message = Date.now() - time_last_message;
                // Only update after 1 second
                if (time_since_last_message > 1000) {
                    // Update the document with the response
                    this.reply = data.response_text;
                    this.editorData = data.document_json;
                    this.editorUpdate()
                    time_last_message = Date.now();

                }
            } else if (data.status == "end") {
                // Stream finished, update the document
                console.log("Stream end", instruction);    
                this.editorData = data.document_json;
                this.reply = data.response_text;
                this.editorUpdate(true);
                //this.task.documentReady();
                instruction.setState({"status":"idle"});
                this.setState({"status": "idle"})
                socket.close();
            };
        };
    
        socket.onerror = function (error) {
            console.log(`[error] ${error.message}`);
            socket.close();
        };
    
    }

    save_back(document_id, output_data, json=true) {
        console.log("document_save_back", document_id);
        let csrfToken = Cookies.get('csrftoken');
        let url = `/document/api/v1/document/${document_id}/save`
        let document_reply = null;
        let document_json = null;
        if (json) {
            document_json = JSON.stringify(output_data);
        } else {
            document_reply = output_data;
        }
        console.log(document_json);
        console.log(document_reply);
        jQuery.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrfToken,
                'document_reply': document_reply,
                'document_json': document_json
            },
            dataType: 'json',
            success: (data) => {
                console.log('Document saved successfully: ', data)
            },
            error: (jqXHR, textStatus, errorThrown) => {
                console.log('Error: ', textStatus)
                console.log('Saving document failed: ', errorThrown)
                //console.log('Server response: ', jqXHR.responseText)
            }
        })
    }
    
    save(document_id) {
        console.log("save", document_id)
        if (!this.editorJS) {
            this.save_back(document_id, this.reply, false);
        } else {
            this.editor.save().then((output_data) => {
                console.log('Document data: ', output_data)
                this.save_back(document_id, output_data)
            }).catch((error) => {
                console.log('Saving document failed: ', error)
            });
        }
    }

    /* Editor editing */

    loadSections() {
        console.log("DocumentComponent.loadSections", this.editorData);
        /* Data is the data returned by EditorJS.save() */
        let blocks = this.editorData.blocks;
        let sections = [];
        let currentSection = null;

        blocks.forEach((block, index) => {
            if (block.type === 'header' && block.data.level === 2) {
                if (currentSection) {
                    sections.push(currentSection);
                }
                currentSection = {
                    header: {"id":block.id, "index":index},
                    elements: []
                };
            } else if (currentSection) {
                currentSection.elements.push({"id":block.id, "index":index});
            }
        });

        // Pushing the last section if exists
        if (currentSection) {
            sections.push(currentSection);
        }

        this.sections = sections;

        // Push section data to backend
        jQuery.ajax({
            url: `/document/${this.state.id}/sections/save`,
            type: 'POST',
            data: {
                'sections': JSON.stringify(this.sections),
                'csrfmiddlewaretoken': Cookies.get('csrftoken')
            },
            dataType: 'json',
            success: (data) => {
                console.log('Sections saved successfully: ', data)
            },
            error: (jqXHR, textStatus, errorThrown) => {
                console.log('Saving sections failed: ', errorThrown)
            }
        })
    }

    selectSection(sectionIndex, scroll=false) {
        console.log("DocumentComponent.selectSection", sectionIndex, scroll);

        // Deselect everything
        this.$element.find(".ce-block").removeClass("ce-block--selected");

        // Find DOM elements that have id's in the section
        let section = this.sections[sectionIndex];
        console.log(section);
        this.$element.find(`.ce-block[data-id="${section.header.id}"]`).each((index, element) => {
            jQuery(element).addClass("ce-block--selected");
        })
        section.elements.forEach((element) => {
            this.$element.find(`.ce-block[data-id="${element.id}"]`).each((index, el) => {
                jQuery(el).addClass("ce-block--selected");
            })
        });
        
        // Scroll to section (done when selecting instruction element of revision)
        if (scroll) this.scrollToSection(sectionIndex);
    }

    getSectionHeader(section) {
        return this.editorData.blocks[section.header.index].data.text;
    }

    scrollToSection(sectionIndex) {
        console.log("scrollToSection", sectionIndex);
        let section = this.sections[sectionIndex];
        var selected = this.$element.find(`.ce-block[data-id="${section.header.id}"]`);
        this.$element.animate({scrollTop: selected[0].offsetTop},'fast');
    }

    isEmpty() {
        if (!this.editorData) return true;
        return this.editorData.blocks.length == 0;
    }

    isReadyForFeedback() {
        if (!this.isEmpty() && this.state["status"] == "idle") {
            return true;
        } else {
            return false;
        }
    }

    /* Render */

    render() {
        this.$element.toggleClass("document--format", this.state["format_open"]);
        this.$header.toggleClass("document__header--format", this.state["format_open"]);
        this.$headerFormatClose.hide();
        this.$headerToolbar.hide();
        

        if (this.state["status"] == "streaming") {
            this.$element.addClass("document--streaming");
            this.$header.addClass("document__header--streaming");
            this.$headerFormats.hide();
            this.$headerLoading.hide()
            this.$headerStreaming.show()
        } else if (this.state["status"] == "loading") {
            this.$element.addClass("document--loading");
            this.$header.addClass("document__header--loading");
            this.$headerFormats.hide();
            this.$headerStreaming.hide();
            this.$headerLoading.show();
        } else {
            // Hide loading
            //jQuery("#project-document-indicator").removeClass("htmx-request");
            // Show document
            //jQuery("#project-document-wrapper").show();            
            this.$element.removeClass("document--streaming");
            this.$header.removeClass("document__header--streaming");
            this.$element.removeClass("document--loading");
            this.$header.removeClass("document__header--loading");
            this.$headerFormats.show();
            this.$headerLoading.hide();
            this.$headerStreaming.hide();
            this.$headerToolbar.toggle(!this.state["format_open"]);
            this.$headerFormatClose.toggle(this.state["format_open"]);
        }
    }
    
}