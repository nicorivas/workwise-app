import AbstractView from '../abstractView.js';
import TableComponent from '../../components/tableComponent/table.js';

export default class FlowsView extends AbstractView {
    
    constructor(element) {
        super(element)
        this.init();
    }

    init() {
        this.flowsTable = new TableComponent("#flows-table", "/flows/")
    }
    
    /**
     * @override
     */
    bindEvents() {
    }
}