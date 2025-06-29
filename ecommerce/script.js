// Instead of using offset, we'll track the current page for each section.
let similarPage = 1; // our initial page (the first 5 items were loaded by the server)
let alsoPage = 1;
const selectedCustomer = "{{ selected_customer }}";

// Function to fetch more products for a given section
async function fetchMore(section) {
    // Calculate the next page number
    let nextPage = section === 'similar' ? similarPage + 1 : alsoPage + 1;
    try {
        const response = await fetch(
            `/load-more-products/?section=${section}&page=${nextPage}&customer_id=${selectedCustomer}`
        );
        const data = await response.json();

        // Determine which list element to append to
        const listElement =
            section === 'similar'
                ? document.getElementById('similar-products-list')
                : document.getElementById('also-products');

        // If no more products are returned, do nothing (or optionally display a message)
        if (data.products.length === 0) {
            return;
        }

        // Append each new product as a list item
        data.products.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item';
            li.textContent = item;
            listElement.appendChild(li);
        });

        // Update the current page tracker
        if (section === 'similar') {
            similarPage = nextPage;
        } else {
            alsoPage = nextPage;
        }
    } catch (err) {
        console.error('Error fetching more products:', err);
    }
}

// Listen for scroll events to trigger the infinite scroll fetch
window.addEventListener('scroll', () => {
    // If the user is near the bottom of the page, fetch more for both sections
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 200) {
        fetchMore('similar');
        fetchMore('also');
    }
});
