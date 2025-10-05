async function cariRekomendasi() {
  const judul = document.getElementById("judul").value;
  const hasilDiv = document.getElementById("hasil");

  if (judul.trim() === "") {
    hasilDiv.innerHTML = "<p>Masukkan judul drama terlebih dahulu!</p>";
    return;
  }

  hasilDiv.innerHTML = "<p>Sedang mencari rekomendasi...</p>";

  try {
    const response = await fetch("/rekomendasi", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ judul }),
    });

    const data = await response.json();
    const rekomendasi = data.rekomendasi;

    let hasilHTML = `<h3>Rekomendasi mirip dengan "${judul}":</h3>`;
    rekomendasi.forEach((drama) => {
      hasilHTML += `<div class="hasil-item">${drama}</div>`;
    });

    hasilDiv.innerHTML = hasilHTML;
  } catch (error) {
    hasilDiv.innerHTML = "<p>Terjadi kesalahan saat mengambil data.</p>";
  }
}
