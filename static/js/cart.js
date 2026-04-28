const cartOffcanvas = document.getElementById("offcanvasCart");
if (cartOffcanvas) {
  cartOffcanvas.addEventListener("show.bs.offcanvas", function () {
    fetchCart();
  });
}

function fetchCart() {
  const container = document.getElementById("cart-items-container");
  const totalEl = document.getElementById("cart-total");

  fetch("/api/cart")
    .then((response) => response.json())
    .then((data) => {
      if (!data.items || data.items.length === 0) {
        container.innerHTML =
          '<p style="font-size:14px; color: var(--color-muted);">Корзина пуста</p>';
        if (totalEl) totalEl.textContent = "0 ₽";
        updateCartCount(0);
        return;
      }

      const html = data.items
        .map(
          (item) => `
        <div class="cart-item">
          <div class="d-flex justify-content-between align-items-start">
            <span class="cart-item__name">${item.product_name}</span>
            <div class="d-flex align-items-center gap-2">
              <span class="cart-item__price">${item.subtotal} ₽</span>
              <button class="btn btn-sm text-muted p-0 border-0 ms-2" onclick="deleteCartItem(${item.id})" title="Удалить">
                <i class="bi bi-x-lg"></i>
              </button>
            </div>
          </div>
          <div style="font-size:12px; color: var(--color-muted); margin-top:0.25rem;">
            ${item.quantity} шт. × ${item.price} ₽
          </div>
        </div>`
        )
        .join("");

      container.innerHTML = html;
      if (totalEl) totalEl.textContent = `${data.total} ₽`;
      updateCartCount(data.items_count);
    })
    .catch(() => {
      if (container) {
        container.innerHTML =
          '<p style="font-size:14px; color: var(--color-error);">Ошибка загрузки корзины</p>';
      }
    });
}

function updateCartCount(count) {
  const countEl = document.getElementById("cart-count");
  if (countEl) countEl.textContent = count;
}

function deleteCartItem(itemId) {
  fetch(`/api/cart/${itemId}`, { method: "DELETE" })
    .then((response) => response.json())
    .then(() => {
      fetchCart();
    })
    .catch((error) => console.error("Ошибка при удалении товара:", error));
}
