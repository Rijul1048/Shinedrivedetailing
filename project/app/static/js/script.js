document.addEventListener("DOMContentLoaded", function () {
  // Mobile menu toggle
  const menuBtn = document.getElementById('menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');

  menuBtn.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
  });

  // Navbar scroll effect
  const navbar = document.getElementById('navbar');

  window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
      // When scrolled, add a solid background and shadow
      navbar.classList.add('bg-white', 'shadow-md');
      navbar.classList.remove('nav-glass'); // Remove glass effect
    } else {
      // At top, use initial transparent/glass effect
      navbar.classList.remove('bg-white', 'shadow-md');
      navbar.classList.add('nav-glass');
    }
  });

  // New function to create floating particles for the new hero section
  function createNewParticles() {
    const container = document.getElementById('new-particles-container');
    const particleCount = 15; // Fewer, larger particles for a cleaner look

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.classList.add('new-particle');

      const size = Math.random() * 30 + 10; // Larger particles
      const startX = Math.random() * 100;
      const startY = Math.random() * 100;

      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${startX}%`;
      particle.style.top = `${startY}%`;
      particle.style.opacity = Math.random() * 0.3 + 0.1; // More subtle opacity

      // Randomize animation duration and delay
      particle.style.animationDuration = `${Math.random() * 10 + 10}s`;
      particle.style.animationDelay = `${Math.random() * 8}s`;

      container.appendChild(particle);
    }
  }

  // Initialize new particles when the DOM is loaded
  document.addEventListener('DOMContentLoaded', () => {
    createNewParticles();
  });
  // ===== Package Tabs =====
  const tabBtns = document.querySelectorAll(".tab-btn");
  const packageCards = document.querySelectorAll(".package-card");

  if (tabBtns.length > 0 && packageCards.length > 0) {
    function handleTabClick(e) {
      tabBtns.forEach((btn) => {
        btn.classList.remove("active", "bg-[#756AB6]", "text-white");
        btn.classList.add("bg-white", "text-[#756AB6]", "border");
      });

      this.classList.add("active", "bg-[#756AB6]", "text-white");
      this.classList.remove("bg-white", "text-[#756AB6]", "border");

      const tabName = this.dataset.tab;

      packageCards.forEach((card) => {
        card.classList.add("hidden");
      });

      if (tabName === "full") {
        document.querySelectorAll(".full-detail").forEach((card) => {
          card.classList.remove("hidden");
        });
      } else if (tabName === "exterior") {
        document.querySelectorAll(".exterior-detail").forEach((card) => {
          card.classList.remove("hidden");
        });
      } else if (tabName === "interior") {
        document.querySelectorAll(".interior-detail").forEach((card) => {
          card.classList.remove("hidden");
        });
      }
    }

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", handleTabClick);
    });

    // Activate first tab
    tabBtns[0].click();
  }

  // ===== Back to Top Button =====
  const backToTopButton = document.getElementById("back-to-top");
  if (backToTopButton) {
    window.addEventListener("scroll", function () {
      if (window.pageYOffset > 300) {
        backToTopButton.classList.remove("opacity-0", "invisible");
        backToTopButton.classList.add("opacity-100", "visible");
      } else {
        backToTopButton.classList.remove("opacity-100", "visible");
        backToTopButton.classList.add("opacity-0", "invisible");
      }
    });

    backToTopButton.addEventListener("click", function () {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  // ===== Smooth Scrolling =====
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });
});

// ===== Google Maps Reviews =====
let reviewsInitialized = false; // Flag to track initialization

function initMap() {
  // Prevent multiple initializations
  if (reviewsInitialized) return;
  reviewsInitialized = true;

  const summaryContainer = document.getElementById("review-summary");
  const reviewsTrack = document.getElementById("reviews-track");

  if (!summaryContainer || !reviewsTrack) return;

  // Clear existing elements
  summaryContainer.innerHTML = "";
  reviewsTrack.innerHTML = "";

  // Remove any existing "Read All" links
  const existingLinks = document.querySelectorAll(".reviews-link");
  existingLinks.forEach((link) => link.remove());

  const service = new google.maps.places.PlacesService(
    document.createElement("div")
  );

  service.getDetails(
    {
      placeId: "ChIJH4rkzU6ph0cR5YBNx_aKv2A",
      fields: ["name", "rating", "reviews", "url", "user_ratings_total"],
    },
    (place, status) => {
      if (status === google.maps.places.PlacesServiceStatus.OK && place) {
        const totalReviews = place.user_ratings_total || 0;
        const overallRating = place.rating || "N/A";

        summaryContainer.innerHTML = `
        <h3 class="text-2xl font-bold mb-4 text-[#756AB6]">Rated ${overallRating}/5 ⭐</h3>
        <p class="text-lg text-[#756AB6]">Trusted by <strong class="text-[#7F55B1] text-2xl">${totalReviews}+</strong> happy customers</p>
      `;

        if (place.reviews && place.reviews.length > 0) {
          // Don't duplicate reviews array - show original set only
          reviewsTrack.innerHTML = place.reviews
            .map(
              (r) => `
          <div class="bg-gradient-to-r from-[#756AB6] to-[#5f52a9] p-8 rounded-xl min-w-[300px] md:min-w-[400px] max-w-[400px] border border-[#7F55B1] shadow-sm h-auto flex flex-col backdrop-blur-sm hover:border-purple-400 transition-all duration-300">
            <div class="font-bold text-[#E8F9FF] text-lg mb-2">${r.author_name
                }</div>
            <div class="text-[#7F55B1] text-lg mb-4">${"⭐".repeat(
                  r.rating
                )} • ${r.rating}/5</div>
            <p class="text-[#E8F9FF] leading-relaxed text-base flex-grow">"${r.text
                }"</p>
          </div>
        `
            )
            .join("");

          if (place.url) {
            // Create link with unique class
            const link = document.createElement("div");
            link.className = "reviews-link text-center mt-8";
            link.innerHTML = `
            <a href="${place.url}" target="_blank" rel="noopener noreferrer" 
              class="text-[#7F55B1] no-underline border-2 border-[#7F55B1] py-3 px-6 rounded-full transition-all duration-300 font-bold inline-block hover:bg-[#7F55B1] hover:text-white hover:shadow-lg hover:shadow-[#7F55B1]/30">
              Read All ${totalReviews} Reviews
            </a>
          `;
            reviewsTrack.after(link); // Insert after reviews track
          }
        } else {
          reviewsTrack.innerHTML =
            '<div class="text-[#E8F9FF] text-center py-5">Our customers love us! Check back soon for more reviews.</div>';
        }
      } else {
        summaryContainer.innerHTML = `
        <div class="text-[#E8F4E2]">
          <h3 class="text-2xl font-bold mb-2 text-[#7F55B1]">Our Customers Love Us!</h3>
          <p>While we load our latest reviews, here's what people say:</p>
        </div>
      `;

        reviewsTrack.innerHTML = `
        <div class="bg-[#756AB6] p-6 md:p-8 rounded-xl min-w-[300px] md:min-w-[400px] max-w-[400px] border border-[#7F55B1] shadow-sm h-auto flex flex-col backdrop-blur-sm">
          <div class="font-bold text-[#7F55B1] text-lg mb-2">Sarah M.</div>
          <div class="text-[#7F55B1] text-lg mb-4">⭐⭐⭐⭐⭐ • 5/5</div>
          <p class="text-[#E8F9FF] leading-relaxed text-base flex-grow">"The best detailing service I've ever used! My car looks brand new again."</p>
        </div>
      `;
      }
    }
  );
}
// ===== Google Maps Reviews =====
// Modified API loader with single execution
function loadReviews() {
  if (typeof google === "undefined") {
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyB6iCfwC2HzjH_RUeB3h8l94lgyZM0_wEg&libraries=places&callback=initMap`;
    script.async = true;
    script.defer = true;
    script.id = "google-maps-script";
    document.head.appendChild(script);
  } else if (!reviewsInitialized) {
    initMap();
  }
}

// Initialize only if the section exists
if (document.getElementById("review-summary")) {
  loadReviews();
}
document.addEventListener("DOMContentLoaded", function () {
  // ===== FAQ Toggle =====
  const faqToggles = document.querySelectorAll(".faq-toggle");
  if (faqToggles.length > 0) {
    faqToggles.forEach((toggle) => {
      toggle.addEventListener("click", function () {
        const content = this.nextElementSibling;
        const icon = this.querySelector("svg");

        if (content && icon) {
          content.classList.toggle("hidden");
          icon.classList.toggle("rotate-180");

          // Close other FAQs when one opens
          if (!content.classList.contains("hidden")) {
            faqToggles.forEach((otherToggle) => {
              if (otherToggle !== toggle) {
                const otherContent = otherToggle.nextElementSibling;
                const otherIcon = otherToggle.querySelector("svg");
                otherContent.classList.add("hidden");
                otherIcon.classList.remove("rotate-180");
              }
            });
          }
        }
      });
    });
  }

  // ===== Before/After Slider =====
  const beforeAfterSliders = document.querySelectorAll(".before-after-slider");
  if (beforeAfterSliders.length > 0) {
    beforeAfterSliders.forEach((container) => {
      const slider = container.querySelector('input[type="range"]');
      const afterImage = container.querySelector(".after-image");
      const handle = container.querySelector(".slider-handle");
      const line = container.querySelector(".slider-line");

      if (slider && afterImage && handle && line) {
        function updateSlider(value) {
          const percent = value || slider.value;
          afterImage.style.clipPath = `inset(0 ${100 - percent}% 0 0)`;
          handle.style.left = `${percent}%`;
          line.style.left = `${percent}%`;
        }

        // Initialize slider
        updateSlider(50);

        // Input event for range slider
        slider.addEventListener("input", () => updateSlider());

        // Touch events for mobile
        let isDragging = false;
        let startX = 0;
        let currentX = 0;

        container.addEventListener(
          "touchstart",
          (e) => {
            isDragging = true;
            startX = e.touches[0].clientX;
            currentX = startX;
            e.preventDefault();
          },
          { passive: false }
        );

        container.addEventListener("touchend", () => {
          isDragging = false;
        });

        container.addEventListener("touchmove", (e) => {
          if (!isDragging) return;
          e.preventDefault();

          const touchX = e.touches[0].clientX;
          const moveX = touchX - currentX;
          currentX = touchX;

          const rect = container.getBoundingClientRect();
          const currentPercent = parseFloat(handle.style.left);
          const newPercent = Math.min(
            100,
            Math.max(0, currentPercent + (moveX / rect.width) * 100)
          );

          slider.value = newPercent;
          updateSlider(newPercent);
        });

        // Mouse events for desktop
        container.addEventListener("mousedown", (e) => {
          isDragging = true;
          startX = e.clientX;
          currentX = startX;
          e.preventDefault();
        });

        window.addEventListener("mouseup", () => {
          isDragging = false;
        });

        window.addEventListener("mousemove", (e) => {
          if (!isDragging) return;

          const mouseX = e.clientX;
          const moveX = mouseX - currentX;
          currentX = mouseX;

          const rect = container.getBoundingClientRect();
          const currentPercent = parseFloat(handle.style.left);
          const newPercent = Math.min(
            100,
            Math.max(0, currentPercent + (moveX / rect.width) * 100)
          );

          slider.value = newPercent;
          updateSlider(newPercent);
        });
      }
    });
  }

  // ===== Package Switcher =====
  const packageBtns = document.querySelectorAll(".package-btn");
  if (packageBtns.length > 0) {
    packageBtns.forEach((btn) => {
      btn.addEventListener("click", function () {
        const packageType = this.dataset.package;

        // Update button states
        packageBtns.forEach((b) => {
          b.classList.remove("bg-[#756AB6]", "text-white", "shadow-md");
          b.classList.add("bg-white", "text-[#756AB6]", "shadow-sm");
        });

        this.classList.add("bg-[#756AB6]", "text-white", "shadow-md");
        this.classList.remove("bg-white", "text-[#756AB6]", "shadow-sm");

        // Show selected content
        document.querySelectorAll(".process-content").forEach((content) => {
          if (content) {
            content.classList.toggle(
              "hidden",
              content.dataset.process !== packageType
            );
          }
        });
      });
    });

    // Activate first button by default
    packageBtns[0].click();
  }
});

// Load Google Maps API
function loadGoogleMaps() {
  if (typeof google === "undefined") {
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places&callback=initMap`;
    script.async = true;
    script.defer = true;
    document.head.appendChild(script);
  } else {
    initMap();
  }
}

// Initialize after full load
window.addEventListener("load", function () {
  const preloader = document.getElementById('preloader');
  if (preloader) {
    preloader.style.display = 'none';
  }
  if (document.getElementById("review-summary")) {
    loadGoogleMaps();
  }
});
document.addEventListener("DOMContentLoaded", function () {
  // Get URL parameters
  const urlParams = new URLSearchParams(window.location.search);
  const vehicleType = urlParams.get("vehicle") || "sedan";
  const serviceType = urlParams.get("service") || "full";
  const packageType = urlParams.get("package") || "gold_full";

  // Set vehicle type display and hidden value
  const vehicleDisplayMap = {
    sedan: "Sedan/Coupe (2 Seats)",
    suv5: "SUV (5 Seats)",
    suv7: "Pick Up/7-Seat SUV",
    xlsuv: "XL SUV",
  };

  document.getElementById("displayVehicleType").textContent =
    vehicleDisplayMap[vehicleType] || "Sedan/Coupe (2 Seats)";
  document.getElementById("id_vehicle_type").value = vehicleType;

  // Set service type display and hidden value
  const serviceDisplayMap = {
    full: "Full Detail (Interior + Exterior)",
    interior: "Interior Detail",
    exterior: "Exterior Detail",
  };

  document.getElementById("displayServiceType").textContent =
    serviceDisplayMap[serviceType] || "Full Detail (Interior + Exterior)";
  document.getElementById("id_service_type").value = serviceType;

  // Set package display and hidden values based on vehicle and package type
  const packageInfo = getPackageInfo(vehicleType, serviceType, packageType);
  document.getElementById("displayPackage").textContent = packageInfo.display;
  document.getElementById("id_package_type").value = packageType.split('_')[0]; // Changed to packageType.split('_')[0]
  document.getElementById("packagePrice").value = packageInfo.price;

  // Update summary section
  updateSummary(vehicleType, serviceType, packageType);

  // Set minimum date to today
  const today = new Date();
  const dd = String(today.getDate()).padStart(2, "0");
  const mm = String(today.getMonth() + 1).padStart(2, "0");
  const yyyy = today.getFullYear();
  document.getElementById("id_date").min = `${yyyy}-${mm}-${dd}`;
});

function getPackageInfo(vehicleType, serviceType, packageType) {
  // Define pricing and display info for all vehicle and package combinations
  const pricing = {
    sedan: {
      full: {
        bronze_full: {
          display: "Bronze Full Detail ($136 CAD)",
          price: "136",
          duration: "1-2 hours",
        },
        gold_full: {
          display: "Gold Full Detail ($195 CAD)",
          price: "195",
          duration: "2-3 hours",
        },
        platinum_full: {
          display: "Platinum Full Detail ($217 CAD)",
          price: "217",
          duration: "3-4 hours",
        },
      },
      interior: {
        bronze_interior: {
          display: "Bronze Interior Detail ($110 CAD)",
          price: "110",
          duration: "1-1.5 hours",
        },
        gold_interior: {
          display: "Gold Interior Detail ($165 CAD)",
          price: "165",
          duration: "1.5-2.5 hours",
        },
        platinum_interior: {
          display: "Platinum Interior Detail ($186 CAD)",
          price: "186",
          duration: "2-3 hours",
        },
      },
      exterior: {
        gold_exterior: {
          display: "Gold Exterior Detail ($163 CAD)",
          price: "163",
          duration: "1-1.5 hours",
        },
        platinum_exterior: {
          display: "Premium Exterior Detail ($200 CAD)",
          price: "200",
          duration: "1.5-2 hours",
        },
      },
    },
    suv5: {
      full: {
        bronze_full: {
          display: "Bronze Full Detail ($171 CAD)",
          price: "171",
          duration: "1.5-2.5 hours",
        },
        gold_full: {
          display: "Gold Full Detail ($217 CAD)",
          price: "217",
          duration: "2.5-3.5 hours",
        },
        platinum_full: {
          display: "Platinum Full Detail ($244 CAD)",
          price: "244",
          duration: "3.5-4.5 hours",
        },
      },
      interior: {
        bronze_interior: {
          display: "Bronze Interior Detail ($137 CAD)",
          price: "137",
          duration: "1.5-2 hours",
        },
        gold_interior: {
          display: "Gold Interior Detail ($181 CAD)",
          price: "181",
          duration: "2-2.5 hours",
        },
        platinum_interior: {
          display: "Platinum Interior Detail ($208 CAD)",
          price: "208",
          duration: "2.5-3.5 hours",
        },
      },
      exterior: {
        gold_exterior: {
          display: "Gold Exterior Detail ($181 CAD)",
          price: "181",
          duration: "1-2 hours",
        },
        platinum_exterior: {
          display: "Premium Exterior Detail ($228 CAD)",
          price: "228",
          duration: "1.5-2.5 hours",
        },
      },
    },
    suv7: {
      full: {
        bronze_full: {
          display: "Bronze Full Detail ($204 CAD)",
          price: "204",
          duration: "2-3 hours",
        },
        gold_full: {
          display: "Gold Full Detail ($258 CAD)",
          price: "258",
          duration: "3-4 hours",
        },
        platinum_full: {
          display: "Platinum Full Detail ($285 CAD)",
          price: "285",
          duration: "4-5 hours",
        },
      },
      interior: {
        bronze_interior: {
          display: "Bronze Interior Detail ($154 CAD)",
          price: "154",
          duration: "2-2.5 hours",
        },
        gold_interior: {
          display: "Gold Interior Detail ($208 CAD)",
          price: "208",
          duration: "2.5-3 hours",
        },
        platinum_interior: {
          display: "Platinum Interior Detail ($235 CAD)",
          price: "235",
          duration: "3-4 hours",
        },
      },
      exterior: {
        gold_exterior: {
          display: "Gold Exterior Detail ($200 CAD)",
          price: "200",
          duration: "1.5-2 hours",
        },
        platinum_exterior: {
          display: "Premium Exterior Detail ($250 CAD)",
          price: "250",
          duration: "2-2.5 hours",
        },
      },
    },
    xlsuv: {
      full: {
        bronze_full: {
          display: "Bronze Full Detail ($213 CAD)",
          price: "213",
          duration: "2.5-3.5 hours",
        },
        gold_full: {
          display: "Gold Full Detail ($267 CAD)",
          price: "267",
          duration: "3.5-4.5 hours",
        },
        platinum_full: {
          display: "Platinum Full Detail ($294 CAD)",
          price: "294",
          duration: "4.5-6 hours",
        },
      },
      interior: {
        bronze_interior: {
          display: "Bronze Interior Detail ($163 CAD)",
          price: "163",
          duration: "2.5-3 hours",
        },
        gold_interior: {
          display: "Gold Interior Detail ($217 CAD)",
          price: "217",
          duration: "3-3.5 hours",
        },
        platinum_interior: {
          display: "Platinum Interior Detail ($244 CAD)",
          price: "244",
          duration: "3.5-4.5 hours",
        },
      },
      exterior: {
        gold_exterior: {
          display: "Gold Exterior Detail ($213 CAD)",
          price: "213",
          duration: "2-2.5 hours",
        },
        platinum_exterior: {
          display: "Premium Exterior Detail ($286 CAD)",
          price: "286",
          duration: "2.5-3 hours",
        },
      },
    },
  };

  return (
    pricing[vehicleType]?.[serviceType]?.[packageType] ||
    pricing["sedan"]["full"]["gold_full"]
  );
}

// KEEP THIS PART (it's essential for your page):
function updateSummary(vehicleType, serviceType, packageType) {
  const packageInfo = getPackageInfo(vehicleType, serviceType, packageType);
  const vehicleDisplayMap = {
    sedan: "Sedan/Coupe (2 Seats)",
    suv5: "SUV (5 Seats)",
    suv7: "Pick Up/7-Seat SUV",
    xlsuv: "XL SUV",
  };
  const serviceDisplayMap = {
    full: "Full Detail",
    interior: "Interior Detail",
    exterior: "Exterior Detail",
  };

  document.getElementById("summaryService").textContent =
    packageInfo.display.split(" (")[0];
  document.getElementById("summaryVehicle").textContent =
    vehicleDisplayMap[vehicleType] || "Sedan/Coupe (2 Seats)";
  document.getElementById("summaryDuration").textContent = packageInfo.duration;
  document.getElementById(
    "summaryTotal"
  ).textContent = `$${packageInfo.price} CAD`;
}

// aboutus

document.addEventListener('DOMContentLoaded', function () {
  const galleryItems = document.querySelectorAll('.group.relative');

  galleryItems.forEach(item => {
    item.addEventListener('click', function () {
      const imgSrc = this.querySelector('img').src;
      const title = this.querySelector('h3').textContent;
      const description = this.querySelector('p').textContent;

      // Create lightbox overlay
      const lightbox = document.createElement('div');
      lightbox.className = 'fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4';
      lightbox.innerHTML = `
          <div class="relative max-w-4xl w-full">
            <img src="${imgSrc}" alt="${title}" class="w-full max-h-[80vh] object-contain">
            <div class="bg-[#FBFBFB] p-4 rounded-b-lg">
              <h3 class="text-xl font-bold text-[#756AB6]">${title}</h3>
              <p class="text-gray-600">${description}</p>
            </div>
            <button class="absolute -top-12 right-0 text-white hover:text-[#AC87C5] transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        `;

      // Add to DOM
      document.body.appendChild(lightbox);

      // Close lightbox
      lightbox.querySelector('button').addEventListener('click', function () {
        document.body.removeChild(lightbox);
      });

      // Close on click outside
      lightbox.addEventListener('click', function (e) {
        if (e.target === this) {
          document.body.removeChild(lightbox);
        }
      });
    });
  });
});

// Reels
const reelContainer = document.getElementById("reelContainer");
if (reelContainer) {
  const reels = Array.from(reelContainer.getElementsByClassName("reel"));
  const prevReel = document.getElementById("prevReel");
  const nextReel = document.getElementById("nextReel");

  if (reels.length > 0 && prevReel && nextReel) {
    let activeIndex = 1;

    function updateReels() {
      reels.forEach((reel, index) => {
        const diff = index - activeIndex;
        const video = reel.querySelector("video");

        if (diff === 0) {
          reel.style.transform = "translateX(0) scale(1)";
          reel.style.zIndex = "20";
          if (video) video.play();
        } else if (diff === -1 || diff === 1) {
          reel.style.transform = `translateX(0) scale(0.75)`;
          reel.style.zIndex = "10";
          if (video) video.pause();
        } else {
          reel.style.transform = "translateX(0) scale(0.5)";
          reel.style.zIndex = "0";
          if (video) video.pause();
        }
      });
    }

    function moveReels(direction) {
      activeIndex = (activeIndex + direction + reels.length) % reels.length;
      updateReels();
    }

    prevReel.addEventListener("click", () => moveReels(-1));
    nextReel.addEventListener("click", () => moveReels(1));

    reels.forEach((reel) => {
      reel.addEventListener("click", () => {
        const clickedIndex = reels.indexOf(reel);
        const diff = clickedIndex - activeIndex;
        moveReels(diff);
      });
    });

    updateReels();
  }
}

// Mobile Reels
const mobileReels = document.getElementById("mobileReels");
if (mobileReels) {
  let currentMobileIndex = 0;
  const reelCount = 3;

  function updateMobileCarousel() {
    const offset = -currentMobileIndex * 100;
    mobileReels.style.transform = `translateX(${offset}%)`;

    document.querySelectorAll(".mobile-carousel video").forEach((video, index) => {
      if (video) {
        if (index === currentMobileIndex) {
          video.play();
        } else {
          video.pause();
        }
      }
    });
  }

  const mobileNext = document.getElementById("mobileNext");
  const mobilePrev = document.getElementById("mobilePrev");

  if (mobileNext) {
    mobileNext.addEventListener("click", () => {
      if (currentMobileIndex < reelCount - 1) {
        currentMobileIndex++;
        updateMobileCarousel();
      }
    });
  }

  if (mobilePrev) {
    mobilePrev.addEventListener("click", () => {
      if (currentMobileIndex > 0) {
        currentMobileIndex--;
        updateMobileCarousel();
      }
    });
  }
}

// Mute/Unmute functionality
document.querySelectorAll(".mute-btn").forEach((btn) => {
  btn.addEventListener("click", (e) => {
    const videoContainer = e.target.closest("div");
    if (videoContainer) {
      const video = videoContainer.querySelector("video");
      if (video) {
        video.muted = !video.muted;
        e.target.textContent = video.muted ? "🔇" : "🔊";
      }
    }
  });
});

// Confetti
document.addEventListener("DOMContentLoaded", function () {
  const container = document.getElementById("confetti-container");
  const colors = ["#AC87C5", "#756AB6", "#E0E7FF", "#F5F3FF"];

  // Create confetti elements
  for (let i = 0; i < 50; i++) {
    const confetti = document.createElement("div");
    confetti.className = "confetti";
    confetti.style.left = Math.random() * 100 + "vw";
    confetti.style.animationDelay = Math.random() * 5 + "s";
    confetti.style.width = Math.random() * 8 + 5 + "px";
    confetti.style.height = confetti.style.width;
    confetti.style.backgroundColor =
      colors[Math.floor(Math.random() * colors.length)];
    confetti.style.opacity = Math.random() * 0.5 + 0.3;
    container.appendChild(confetti);
  }
});    