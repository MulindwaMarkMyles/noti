const menuButton = document.getElementById("js-click")
const menu = document.getElementById("js-menu")
menuButton.addEventListener('click', () => {
	menuButton.classList.toggle("active")
	menu.classList.toggle("active")
	setTimeout(() => {
		menuButton.classList.toggle("active")
		menu.classList.toggle("active")
	}, 3000)
})


const searchButton = document.getElementById("js-search-button")
function search() {
	
}