import AbstractComponent from '../abstractComponent.js';

export default class FlowFormComponent extends AbstractComponent {

  constructor(element) {
    super(element);
    this.state = {
      currentStep: 0,
      steps: [
        '#step-1',
        '#step-2',
        '#step-3',
        '#step-4',
        '#step-5'
      ],
      // Add additional state properties as necessary
    };
  }

  init() {
    this.render();
    this.bindEvents();
  }

  bindEvents() {
    //this.bindEvent('click', this.nextStep, '.next-btn');
  }

  prevStep(component=null) {
    if (component == null) component = this;
    const prevStepIndex = component.state.currentStep - 1;
    if (prevStepIndex >= 0) {
      component.setState({ currentStep: prevStepIndex });
    }
  }

  nextStep(component=null) {
    if (component == null) component = this;
    const nextStepIndex = component.state.currentStep + 1;
    if (nextStepIndex < component.state.steps.length) {
      component.setState({ currentStep: nextStepIndex });
    }
  }

  render() {
    // Hide all steps
    jQuery(this.state.steps.join(', ')).hide();

    // Show the current step
    jQuery(this.state.steps[this.state.currentStep]).show();

    // Update step indicator
    jQuery('.step-indicator .dot').removeClass('active');
    jQuery(`.step-indicator .dot:eq(${this.state.currentStep})`).addClass('active');
  }

  destroy() {
    this.unbindEvent('click', '.next-btn');
  }
}