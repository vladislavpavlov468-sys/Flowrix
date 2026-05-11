const cartOffcanvas = document.getElementById("offcanvasCart");
if (cartOffcanvas) {
  cartOffcanvas.addEventListener("show.bs.offcanvas", function () {
    fetchCart();
  });
}

const btnClearCart = document.getElementById("btn-clear-cart");
if (btnClearCart) {
  btnClearCart.addEventListener("click", function () {
    fetch("/api/cart", { method: "DELETE" })
      .then((response) => response.json())
      .then(() => {
        fetchCart();
      })
      .catch((error) => console.error("Ошибка при очистке корзины:", error));
  });
}

function fetchCart() {
  const container = document.getElementById("cart-items-container");
  const totalEl = document.getElementById("cart-total");
  const emptyMessage = document.getElementById("cart-empty-message");
  const footer = document.getElementById("cart-footer");

  fetch("/api/cart")
    .then((response) => response.json())
    .then((data) => {
      if (!data.items || data.items.length === 0) {
        container.innerHTML = "";
        container.classList.add("d-none");
        if (emptyMessage) emptyMessage.classList.remove("d-none");
        if (footer) footer.classList.add("d-none");
        if (totalEl) totalEl.textContent = "0 ₽";
        updateCartCount(0);
        return;
      }

      container.classList.remove("d-none");
      if (emptyMessage) emptyMessage.classList.add("d-none");
      if (footer) footer.classList.remove("d-none");

      const html = data.items
        .map(
          (item) => `
        <div class="cart-item d-flex gap-3 mb-4 align-items-center">
          <div class="cart-item-img bg-surface" style="width: 80px; height: 80px; flex-shrink: 0;">
            ${item.product_image ? `<img src="/uploads/${item.product_image}" style="width:100%; height:100%; object-fit:cover;">` : `<div class="d-flex align-items-center justify-content-center h-100 text-muted"><i class="bi bi-box"></i></div>`}
          </div>
          <div class="flex-grow-1">
            <div class="d-flex justify-content-between align-items-start mb-1">
              <span class="fw-medium" style="font-size: 14px; color: #111;">${item.product_name}</span>
              <button class="btn btn-sm text-muted p-0 border-0" onclick="deleteCartItem(${item.id})" title="Удалить">
                <i class="bi bi-x"></i>
              </button>
            </div>
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center gap-2 border px-2 py-1" style="border-radius: 4px;">
                <button class="cart-qty-btn" onclick="changeQuantity(${item.id}, -1)">-</button>
                <span style="font-size: 14px; min-width: 20px; text-align: center;">${item.quantity}</span>
                <button class="cart-qty-btn" onclick="changeQuantity(${item.id}, 1)">+</button>
              </div>
              <span class="fw-bold" style="font-size: 14px;">${item.subtotal} ₽</span>
            </div>
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

function changeQuantity(itemId, delta) {
  fetch(`/api/cart/${itemId}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ delta: delta }),
  })
    .then((response) => response.json())
    .then(() => {
      fetchCart();
    })
    .catch((error) => console.error("Ошибка при изменении количества:", error));
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
