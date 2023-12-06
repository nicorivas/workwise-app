import AbstractView from '../abstractView.js';
import HeaderComponent from '../../components/headerComponent/header.js';
import SidebarComponent from '../../components/sidebarComponent/sidebar.js';
import HelpSidebarComponent from '../../components/helpSidebarComponent/helpSidebar.js';

export default class BodyView extends AbstractView {
    
    constructor(element) {
        super(element);
        console.log("BodyView.constructor()");
        this.init();
    }

    init() {
        console.log("BodyView.init()");
        this.loadComponents();
    }

    loadComponents() {
        console.log("BodyView.loadComponents()");

        // Header
        this.headerComponent = new HeaderComponent("#header");
        this.headerComponent.helpButton.bindEvent('click', this.headerHelpButtonHandler, null, this);

        // Sidebar
        this.sidebarComponent = new SidebarComponent("#sidebar");
        this.sidebarComponent.buttonExplorer.bindEvent('click', this.sidebarButtonHandler, null, this, "explorer");
        this.sidebarComponent.buttonProjects.bindEvent('click', this.sidebarButtonHandler, null, this, "projects");
        this.sidebarComponent.buttonActions.bindEvent('click', this.sidebarButtonHandler, null, this, "actions");

        // Others
        this.helpSidebarComponent = new HelpSidebarComponent("#help-sidebar");

        this.bindEvents();
    }

    headerHelpButtonHandler(view) {
        console.log("HeaderComponent.helpHandler()", view);
        view.helpSidebarComponent.setState({"open": !view.helpSidebarComponent.state.open});
    }

    sidebarButtonHandler(view, url) {
        console.log("SidebarComponent.sidebarButtonHandler()", view, url);
        view.sidebarComponent.select(url)
        view.openMain(url)
    }

    openMain(url) {
        jQuery("#main-loader-wrapper").addClass("htmx-request");
        jQuery("#main").addClass("htmx-request");
        this.sidebarComponent.select(url)
        jQuery.ajax({
            url: `/${url}/?source=menu`,
            type: "GET",
            success: function(data) {
                jQuery("#main").html(data);
                window.history.pushState("", "", `/${url}/`);
                jQuery("#main-loader-wrapper").removeClass("htmx-request");
                jQuery("#main").removeClass("htmx-request");
            }
        });
    }

    bindEvents() {
        console.log("BodyView.bindEvents()");
    }

    render() {
        console.log("BodyView.render()", this.data);
    }
}