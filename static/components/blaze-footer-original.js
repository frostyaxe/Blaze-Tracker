class BlazeFooter extends HTMLElement {
	
	connectedCallback() {
    this.innerHTML = `<footer id="sticky-footer" class="flex-shrink-0 py-4 bg-dark text-white-50">
		    <div class="container text-center">
		      <small>&copy; 2022 Copyright Abhishek Prajapati, Frostyaxe. All Rights Reserved.</small>
		    </div>
  	    </footer>`;
  }
	
}

customElements.define('blaze-footer', BlazeFooter);