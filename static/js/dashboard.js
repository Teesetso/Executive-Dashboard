const filterButton = document.querySelector('[data-filter]')
const filterPanel = document.querySelector('[data-filter-panel]')
const menuButton = document.querySelector('[data-menu]')
const sidebar = document.querySelector('.sidebar')
const searchButton = document.querySelector('[data-search]')
const notificationButton = document.querySelector('[data-notifications]')
const toast = document.querySelector('[data-toast]')
const siteSearch = document.querySelector('[data-site-search]')
const siteSearchField = document.querySelector('[data-site-search-field]')
const siteRows = [...document.querySelectorAll('[data-site-rows] tr[data-site-name]')]
const siteEmpty = document.querySelector('[data-site-empty]')
const customerSearch = document.querySelector('[data-customer-search]')
const customerSearchField = document.querySelector('[data-customer-search-field]')
const customerRows = [...document.querySelectorAll('[data-customer-rows] tr[data-customer-name]')]
const customerEmpty = document.querySelector('[data-customer-empty]')
const userMenuButton = document.querySelector('[data-user-menu-button]')
const userMenu = document.querySelector('[data-user-menu]')

filterButton?.addEventListener('click', () => filterPanel?.classList.toggle('visible'))
menuButton?.addEventListener('click', () => sidebar?.classList.toggle('visible'))
searchButton?.addEventListener('click', () => document.querySelector('input[name="job_id"]')?.focus())

const filterSites = () => {
	const query = siteSearch?.value.trim().toLowerCase() || ''
	const field = siteSearchField?.value || 'name'
	let visible = 0

	siteRows.forEach((row) => {
		const matches = row.dataset[`site${field[0].toUpperCase()}${field.slice(1)}`]?.includes(query)
		row.hidden = !matches
		if (matches) visible += 1
	})

	if (siteEmpty) siteEmpty.hidden = visible !== 0
}

siteSearch?.addEventListener('input', filterSites)
siteSearchField?.addEventListener('change', filterSites)

const filterCustomers = () => {
	const query = customerSearch?.value.trim().toLowerCase() || ''
	const field = customerSearchField?.value || 'name'
	let visible = 0

	customerRows.forEach((row) => {
		const matches = row.dataset[`customer${field[0].toUpperCase()}${field.slice(1)}`]?.includes(query)
		row.hidden = !matches
		if (matches) visible += 1
	})

	if (customerEmpty) customerEmpty.hidden = visible !== 0
}

customerSearch?.addEventListener('input', filterCustomers)
customerSearchField?.addEventListener('change', filterCustomers)

userMenuButton?.addEventListener('click', (event) => {
	event.stopPropagation()
	const isOpen = !userMenu?.hidden
	if (userMenu) userMenu.hidden = isOpen
	userMenuButton.setAttribute('aria-expanded', String(!isOpen))
})

document.addEventListener('click', () => {
	if (userMenu) userMenu.hidden = true
	userMenuButton?.setAttribute('aria-expanded', 'false')
})

notificationButton?.addEventListener('click', () => {
	if (toast) {
		toast.textContent = 'Notifications are up to date.'
		toast.classList.add('visible')
		window.setTimeout(() => toast.classList.remove('visible'), 2500)
	}
})

document.querySelectorAll('[data-scroll]').forEach((button) => {
	button.addEventListener('click', () => {
		document.getElementById(button.dataset.scroll)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
		if (toast && button.dataset.detail) {
			toast.textContent = `${button.dataset.detail} details are in view.`
			toast.classList.add('visible')
			window.setTimeout(() => toast.classList.remove('visible'), 2500)
		}
	})
})

document.querySelectorAll('.sidebar a').forEach((link) => {
	link.addEventListener('click', () => sidebar?.classList.remove('visible'))
})
