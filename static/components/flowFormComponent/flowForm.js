import AbstractComponent from '../AbstractComponent.js';

export default class FlowFormComponent extends AbstractComponent {

  constructor(element) {
    super(element);
    this.state = {
      currentStep: 0,
      steps: [
        '#step-1',
        '#step-2',
        '#step-3',
        '#step-4'
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

  nextStep() {
    const nextStepIndex = this.state.currentStep + 1;
    if (nextStepIndex < this.state.steps.length) {
      this.setState({ currentStep: nextStepIndex });
    } else {
      // Handle the completion of the last step
      console.log('Form completed');
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