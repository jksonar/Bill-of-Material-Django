/**
 * BOM System - Enhanced UI/UX JavaScript
 * Implements interactive components, animations, accessibility, and real-time feedback
 */

// Global configuration
const BOMSystem = {
  config: {
    animationDuration: 300,
    debounceDelay: 300,
    toastDuration: 5000,
    loadingDelay: 100
  },
  
  // State management
  state: {
    isLoading: false,
    activeModals: [],
    notifications: [],
    theme: localStorage.getItem('bom-theme') || 'light'
  },
  
  // Utility functions
  utils: {
    // Debounce function for performance
    debounce(func, wait) {
      let timeout;
      return function executedFunction(...args) {
        const later = () => {
          clearTimeout(timeout);
          func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
      };
    },
    
    // Throttle function for scroll events
    throttle(func, limit) {
      let inThrottle;
      return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
          func.apply(context, args);
          inThrottle = true;
          setTimeout(() => inThrottle = false, limit);
        }
      };
    },
    
    // Generate unique IDs
    generateId() {
      return 'bom-' + Math.random().toString(36).substr(2, 9);
    },
    
    // Format numbers with commas
    formatNumber(num) {
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    },
    
    // Validate email
    isValidEmail(email) {
      const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return re.test(email);
    },
    
    // Get element by selector with error handling
    getElement(selector) {
      const element = document.querySelector(selector);
      if (!element) {
        console.warn(`Element not found: ${selector}`);
      }
      return element;
    },
    
    // Get elements by selector
    getElements(selector) {
      return document.querySelectorAll(selector);
    }
  }
};

// Animation system
BOMSystem.animations = {
  // Fade in animation
  fadeIn(element, duration = BOMSystem.config.animationDuration) {
    element.style.opacity = '0';
    element.style.display = 'block';
    
    const start = performance.now();
    
    function animate(currentTime) {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      
      element.style.opacity = progress;
      
      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    }
    
    requestAnimationFrame(animate);
  },
  
  // Fade out animation
  fadeOut(element, duration = BOMSystem.config.animationDuration) {
    const start = performance.now();
    const startOpacity = parseFloat(getComputedStyle(element).opacity);
    
    function animate(currentTime) {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      
      element.style.opacity = startOpacity * (1 - progress);
      
      if (progress >= 1) {
        element.style.display = 'none';
      } else {
        requestAnimationFrame(animate);
      }
    }
    
    requestAnimationFrame(animate);
  },
  
  // Slide down animation
  slideDown(element, duration = BOMSystem.config.animationDuration) {
    element.style.height = '0';
    element.style.overflow = 'hidden';
    element.style.display = 'block';
    
    const targetHeight = element.scrollHeight;
    const start = performance.now();
    
    function animate(currentTime) {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      
      element.style.height = (targetHeight * progress) + 'px';
      
      if (progress >= 1) {
        element.style.height = 'auto';
        element.style.overflow = 'visible';
      } else {
        requestAnimationFrame(animate);
      }
    }
    
    requestAnimationFrame(animate);
  },
  
  // Slide up animation
  slideUp(element, duration = BOMSystem.config.animationDuration) {
    const startHeight = element.offsetHeight;
    const start = performance.now();
    
    element.style.overflow = 'hidden';
    
    function animate(currentTime) {
      const elapsed = currentTime - start;
      const progress = Math.min(elapsed / duration, 1);
      
      element.style.height = (startHeight * (1 - progress)) + 'px';
      
      if (progress >= 1) {
        element.style.display = 'none';
        element.style.height = 'auto';
        element.style.overflow = 'visible';
      } else {
        requestAnimationFrame(animate);
      }
    }
    
    requestAnimationFrame(animate);
  },
  
  // Bounce animation
  bounce(element) {
    element.style.animation = 'none';
    element.offsetHeight; // Trigger reflow
    element.style.animation = 'bounce 0.6s ease';
  },
  
  // Shake animation for errors
  shake(element) {
    element.classList.add('micro-shake');
    setTimeout(() => {
      element.classList.remove('micro-shake');
    }, 500);
  },
  
  // Pulse animation
  pulse(element) {
    element.classList.add('pulse');
    setTimeout(() => {
      element.classList.remove('pulse');
    }, 2000);
  }
};

// Notification system
BOMSystem.notifications = {
  container: null,
  
  init() {
    this.container = document.createElement('div');
    this.container.className = 'notification-container';
    this.container.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 1060;
      pointer-events: none;
    `;
    document.body.appendChild(this.container);
  },
  
  show(message, type = 'info', duration = BOMSystem.config.toastDuration) {
    if (!this.container) this.init();
    
    const notification = document.createElement('div');
    const id = BOMSystem.utils.generateId();
    
    notification.className = `alert alert-${type} alert-dismissible fade show notification`;
    notification.style.cssText = `
      pointer-events: auto;
      margin-bottom: 10px;
      min-width: 300px;
      animation: slideInRight 0.3s ease;
    `;
    
    notification.innerHTML = `
      <div class="d-flex align-items-center">
        <div class="flex-grow-1">${message}</div>
        <button type="button" class="btn-close" data-notification-id="${id}" aria-label="Close"></button>
      </div>
    `;
    
    // Add close functionality
    const closeBtn = notification.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
      this.hide(notification);
    });
    
    this.container.appendChild(notification);
    
    // Auto-hide after duration
    if (duration > 0) {
      setTimeout(() => {
        if (notification.parentNode) {
          this.hide(notification);
        }
      }, duration);
    }
    
    return notification;
  },
  
  hide(notification) {
    notification.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 300);
  },
  
  success(message, duration) {
    return this.show(message, 'success', duration);
  },
  
  error(message, duration) {
    return this.show(message, 'danger', duration);
  },
  
  warning(message, duration) {
    return this.show(message, 'warning', duration);
  },
  
  info(message, duration) {
    return this.show(message, 'info', duration);
  }
};

// Loading system
BOMSystem.loading = {
  overlay: null,
  
  show(target = document.body, message = 'Loading...') {
    BOMSystem.state.isLoading = true;
    
    if (!this.overlay) {
      this.overlay = document.createElement('div');
      this.overlay.className = 'loading-overlay';
      this.overlay.innerHTML = `
        <div class="text-center">
          <div class="spinner-custom mb-3"></div>
          <div class="loading-message">${message}</div>
        </div>
      `;
    }
    
    if (target === document.body) {
      this.overlay.style.position = 'fixed';
    } else {
      this.overlay.style.position = 'absolute';
      target.style.position = 'relative';
    }
    
    target.appendChild(this.overlay);
    BOMSystem.animations.fadeIn(this.overlay, 200);
  },
  
  hide() {
    BOMSystem.state.isLoading = false;
    
    if (this.overlay && this.overlay.parentNode) {
      BOMSystem.animations.fadeOut(this.overlay, 200);
      setTimeout(() => {
        if (this.overlay && this.overlay.parentNode) {
          this.overlay.parentNode.removeChild(this.overlay);
        }
      }, 200);
    }
  },
  
  updateMessage(message) {
    if (this.overlay) {
      const messageEl = this.overlay.querySelector('.loading-message');
      if (messageEl) {
        messageEl.textContent = message;
      }
    }
  }
};

// Form enhancements
BOMSystem.forms = {
  init() {
    this.setupValidation();
    this.setupAutoSave();
    this.setupFileUpload();
    this.setupSearchEnhancements();
  },
  
  setupValidation() {
    const forms = BOMSystem.utils.getElements('form[data-validate]');
    
    forms.forEach(form => {
      form.addEventListener('submit', (e) => {
        if (!this.validateForm(form)) {
          e.preventDefault();
          BOMSystem.animations.shake(form);
        }
      });
      
      // Real-time validation
      const inputs = form.querySelectorAll('input, select, textarea');
      inputs.forEach(input => {
        input.addEventListener('blur', () => {
          this.validateField(input);
        });
        
        input.addEventListener('input', BOMSystem.utils.debounce(() => {
          this.validateField(input);
        }, 500));
      });
    });
  },
  
  validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      if (!this.validateField(input)) {
        isValid = false;
      }
    });
    
    return isValid;
  },
  
  validateField(field) {
    const value = field.value.trim();
    const type = field.type;
    const required = field.hasAttribute('required');
    let isValid = true;
    let message = '';
    
    // Remove existing validation classes
    field.classList.remove('is-valid', 'is-invalid');
    
    // Required validation
    if (required && !value) {
      isValid = false;
      message = 'This field is required';
    }
    
    // Type-specific validation
    if (value && type === 'email' && !BOMSystem.utils.isValidEmail(value)) {
      isValid = false;
      message = 'Please enter a valid email address';
    }
    
    if (value && type === 'number') {
      const num = parseFloat(value);
      if (isNaN(num)) {
        isValid = false;
        message = 'Please enter a valid number';
      }
    }
    
    // Custom validation
    const customValidation = field.getAttribute('data-validation');
    if (customValidation && value) {
      const regex = new RegExp(customValidation);
      if (!regex.test(value)) {
        isValid = false;
        message = field.getAttribute('data-validation-message') || 'Invalid format';
      }
    }
    
    // Apply validation classes and feedback
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    let feedback = field.parentNode.querySelector('.invalid-feedback');
    if (!feedback) {
      feedback = document.createElement('div');
      feedback.className = 'invalid-feedback';
      field.parentNode.appendChild(feedback);
    }
    
    feedback.textContent = message;
    feedback.style.display = isValid ? 'none' : 'block';
    
    return isValid;
  },
  
  setupAutoSave() {
    const forms = BOMSystem.utils.getElements('form[data-autosave]');
    
    forms.forEach(form => {
      const inputs = form.querySelectorAll('input, select, textarea');
      
      inputs.forEach(input => {
        input.addEventListener('input', BOMSystem.utils.debounce(() => {
          this.autoSave(form);
        }, 2000));
      });
    });
  },
  
  autoSave(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());
    
    // Save to localStorage
    const formId = form.id || 'autosave-form';
    localStorage.setItem(`autosave-${formId}`, JSON.stringify(data));
    
    // Show auto-save indicator
    let indicator = form.querySelector('.autosave-indicator');
    if (!indicator) {
      indicator = document.createElement('small');
      indicator.className = 'autosave-indicator text-muted';
      indicator.style.cssText = 'position: absolute; top: -20px; right: 0; opacity: 0; transition: opacity 0.3s;';
      form.style.position = 'relative';
      form.appendChild(indicator);
    }
    
    indicator.textContent = 'Draft saved';
    indicator.style.opacity = '1';
    
    setTimeout(() => {
      indicator.style.opacity = '0';
    }, 2000);
  },
  
  setupFileUpload() {
    const fileInputs = BOMSystem.utils.getElements('input[type="file"]');
    
    fileInputs.forEach(input => {
      const wrapper = document.createElement('div');
      wrapper.className = 'file-upload';
      
      input.parentNode.insertBefore(wrapper, input);
      wrapper.appendChild(input);
      
      const label = document.createElement('div');
      label.innerHTML = `
        <div class="file-upload-icon">📁</div>
        <div class="file-upload-text">Click to select files or drag and drop</div>
        <div class="file-upload-hint">Supported formats: ${input.accept || 'All files'}</div>
      `;
      wrapper.appendChild(label);
      
      // Drag and drop functionality
      wrapper.addEventListener('dragover', (e) => {
        e.preventDefault();
        wrapper.classList.add('dragover');
      });
      
      wrapper.addEventListener('dragleave', () => {
        wrapper.classList.remove('dragover');
      });
      
      wrapper.addEventListener('drop', (e) => {
        e.preventDefault();
        wrapper.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          input.files = files;
          this.handleFileSelection(input, files);
        }
      });
      
      input.addEventListener('change', (e) => {
        this.handleFileSelection(input, e.target.files);
      });
    });
  },
  
  handleFileSelection(input, files) {
    const wrapper = input.closest('.file-upload');
    const label = wrapper.querySelector('.file-upload-text');
    
    if (files.length === 1) {
      label.textContent = files[0].name;
    } else if (files.length > 1) {
      label.textContent = `${files.length} files selected`;
    }
    
    // File validation
    Array.from(files).forEach(file => {
      if (input.accept) {
        const acceptedTypes = input.accept.split(',').map(type => type.trim());
        const isValid = acceptedTypes.some(type => {
          if (type.startsWith('.')) {
            return file.name.toLowerCase().endsWith(type.toLowerCase());
          }
          return file.type.match(type.replace('*', '.*'));
        });
        
        if (!isValid) {
          BOMSystem.notifications.error(`File "${file.name}" is not a supported format`);
          return;
        }
      }
      
      // File size validation (10MB default)
      const maxSize = parseInt(input.getAttribute('data-max-size')) || 10 * 1024 * 1024;
      if (file.size > maxSize) {
        BOMSystem.notifications.error(`File "${file.name}" is too large. Maximum size is ${Math.round(maxSize / 1024 / 1024)}MB`);
        return;
      }
    });
  },
  
  setupSearchEnhancements() {
    const searchInputs = BOMSystem.utils.getElements('input[type="search"], input[data-search]');
    
    searchInputs.forEach(input => {
      // Add search icon
      if (!input.parentNode.classList.contains('search-container')) {
        const wrapper = document.createElement('div');
        wrapper.className = 'search-container';
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);
      }
      
      // Add clear button
      const clearBtn = document.createElement('button');
      clearBtn.type = 'button';
      clearBtn.className = 'btn btn-sm btn-outline-secondary search-clear';
      clearBtn.innerHTML = '×';
      clearBtn.style.cssText = `
        position: absolute;
        right: 5px;
        top: 50%;
        transform: translateY(-50%);
        border: none;
        background: none;
        font-size: 18px;
        line-height: 1;
        padding: 0;
        width: 20px;
        height: 20px;
        display: none;
      `;
      
      input.parentNode.appendChild(clearBtn);
      
      // Show/hide clear button
      input.addEventListener('input', () => {
        clearBtn.style.display = input.value ? 'block' : 'none';
      });
      
      // Clear functionality
      clearBtn.addEventListener('click', () => {
        input.value = '';
        input.focus();
        clearBtn.style.display = 'none';
        
        // Trigger input event for HTMX
        input.dispatchEvent(new Event('input', { bubbles: true }));
      });
    });
  }
};

// Table enhancements
BOMSystem.tables = {
  init() {
    this.setupSorting();
    this.setupRowSelection();
    this.setupResponsiveStacking();
  },
  
  setupSorting() {
    const tables = BOMSystem.utils.getElements('table[data-sortable]');
    
    tables.forEach(table => {
      const headers = table.querySelectorAll('th[data-sort]');
      
      headers.forEach(header => {
        header.style.cursor = 'pointer';
        header.innerHTML += ' <span class="sort-indicator">↕️</span>';
        
        header.addEventListener('click', () => {
          this.sortTable(table, header);
        });
      });
    });
  },
  
  sortTable(table, header) {
    const column = header.getAttribute('data-sort');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Determine sort direction
    const currentDirection = header.getAttribute('data-sort-direction') || 'asc';
    const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
    
    // Clear other headers
    table.querySelectorAll('th[data-sort]').forEach(th => {
      th.removeAttribute('data-sort-direction');
      const indicator = th.querySelector('.sort-indicator');
      if (indicator) indicator.textContent = '↕️';
    });
    
    // Set current header
    header.setAttribute('data-sort-direction', newDirection);
    const indicator = header.querySelector('.sort-indicator');
    if (indicator) indicator.textContent = newDirection === 'asc' ? '↑' : '↓';
    
    // Sort rows
    rows.sort((a, b) => {
      const aValue = a.querySelector(`td[data-sort="${column}"]`)?.textContent.trim() || '';
      const bValue = b.querySelector(`td[data-sort="${column}"]`)?.textContent.trim() || '';
      
      // Try to parse as numbers
      const aNum = parseFloat(aValue.replace(/[^\d.-]/g, ''));
      const bNum = parseFloat(bValue.replace(/[^\d.-]/g, ''));
      
      if (!isNaN(aNum) && !isNaN(bNum)) {
        return newDirection === 'asc' ? aNum - bNum : bNum - aNum;
      }
      
      // String comparison
      return newDirection === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue);
    });
    
    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
  },
  
  setupRowSelection() {
    const tables = BOMSystem.utils.getElements('table[data-selectable]');
    
    tables.forEach(table => {
      const rows = table.querySelectorAll('tbody tr');
      
      rows.forEach(row => {
        row.addEventListener('click', (e) => {
          if (e.target.type !== 'checkbox' && e.target.tagName !== 'BUTTON') {
            row.classList.toggle('table-active');
            
            // Emit custom event
            row.dispatchEvent(new CustomEvent('rowSelected', {
              detail: { row, selected: row.classList.contains('table-active') }
            }));
          }
        });
      });
    });
  },
  
  setupResponsiveStacking() {
    const tables = BOMSystem.utils.getElements('table[data-responsive-stack]');
    
    tables.forEach(table => {
      const headers = Array.from(table.querySelectorAll('thead th'));
      const rows = table.querySelectorAll('tbody tr');
      
      rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
          if (headers[index]) {
            cell.setAttribute('data-label', headers[index].textContent.trim());
          }
        });
      });
      
      // Add responsive class
      table.classList.add('table-responsive-stack');
    });
  }
};

// Accessibility enhancements
BOMSystem.accessibility = {
  init() {
    this.setupKeyboardNavigation();
    this.setupFocusManagement();
    this.setupScreenReaderSupport();
    this.setupHighContrastMode();
  },
  
  setupKeyboardNavigation() {
    // Escape key to close modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal.show');
        if (activeModal) {
          const modal = bootstrap.Modal.getInstance(activeModal);
          if (modal) modal.hide();
        }
        
        // Close notifications
        const notifications = BOMSystem.utils.getElements('.notification');
        notifications.forEach(notification => {
          BOMSystem.notifications.hide(notification);
        });
      }
    });
    
    // Tab navigation for custom components
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Tab') {
        this.handleTabNavigation(e);
      }
    });
  },
  
  handleTabNavigation(e) {
    const focusableElements = BOMSystem.utils.getElements(
      'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (e.shiftKey) {
      if (document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      }
    } else {
      if (document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  },
  
  setupFocusManagement() {
    // Focus trap for modals
    document.addEventListener('shown.bs.modal', (e) => {
      const modal = e.target;
      const focusableElements = modal.querySelectorAll(
        'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled])'
      );
      
      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      }
    });
    
    // Restore focus when modal closes
    let lastFocusedElement = null;
    
    document.addEventListener('show.bs.modal', () => {
      lastFocusedElement = document.activeElement;
    });
    
    document.addEventListener('hidden.bs.modal', () => {
      if (lastFocusedElement) {
        lastFocusedElement.focus();
        lastFocusedElement = null;
      }
    });
  },
  
  setupScreenReaderSupport() {
    // Add ARIA labels to interactive elements
    const buttons = BOMSystem.utils.getElements('button:not([aria-label]):not([aria-labelledby])');
    buttons.forEach(button => {
      if (!button.textContent.trim()) {
        const icon = button.querySelector('i, svg');
        if (icon) {
          button.setAttribute('aria-label', 'Button');
        }
      }
    });
    
    // Add live regions for dynamic content
    if (!document.querySelector('#live-region')) {
      const liveRegion = document.createElement('div');
      liveRegion.id = 'live-region';
      liveRegion.setAttribute('aria-live', 'polite');
      liveRegion.setAttribute('aria-atomic', 'true');
      liveRegion.className = 'sr-only';
      document.body.appendChild(liveRegion);
    }
  },
  
  announceToScreenReader(message) {
    const liveRegion = document.querySelector('#live-region');
    if (liveRegion) {
      liveRegion.textContent = message;
      setTimeout(() => {
        liveRegion.textContent = '';
      }, 1000);
    }
  },
  
  setupHighContrastMode() {
    // Detect high contrast preference
    if (window.matchMedia('(prefers-contrast: high)').matches) {
      document.body.classList.add('high-contrast');
    }
    
    // Listen for changes
    window.matchMedia('(prefers-contrast: high)').addEventListener('change', (e) => {
      document.body.classList.toggle('high-contrast', e.matches);
    });
  }
};

// Performance monitoring
BOMSystem.performance = {
  init() {
    this.setupPerformanceObserver();
    this.setupIntersectionObserver();
    this.setupLazyLoading();
  },
  
  setupPerformanceObserver() {
    if ('PerformanceObserver' in window) {
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        entries.forEach(entry => {
          if (entry.entryType === 'navigation') {
            console.log('Page load time:', entry.loadEventEnd - entry.loadEventStart, 'ms');
          }
        });
      });
      
      observer.observe({ entryTypes: ['navigation', 'measure'] });
    }
  },
  
  setupIntersectionObserver() {
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('in-view');
            
            // Lazy load content
            if (entry.target.hasAttribute('data-lazy-load')) {
              this.lazyLoadContent(entry.target);
            }
          }
        });
      }, {
        threshold: 0.1,
        rootMargin: '50px'
      });
      
      // Observe elements with animation classes
      const animatedElements = BOMSystem.utils.getElements('.animate-on-scroll');
      animatedElements.forEach(el => observer.observe(el));
      
      // Observe lazy load elements
      const lazyElements = BOMSystem.utils.getElements('[data-lazy-load]');
      lazyElements.forEach(el => observer.observe(el));
    }
  },
  
  setupLazyLoading() {
    // Lazy load images
    const images = BOMSystem.utils.getElements('img[data-src]');
    images.forEach(img => {
      img.addEventListener('load', () => {
        img.classList.add('loaded');
      });
    });
  },
  
  lazyLoadContent(element) {
    const url = element.getAttribute('data-lazy-load');
    if (url) {
      fetch(url)
        .then(response => response.text())
        .then(html => {
          element.innerHTML = html;
          element.removeAttribute('data-lazy-load');
        })
        .catch(error => {
          console.error('Lazy load failed:', error);
          element.innerHTML = '<p class="text-muted">Content failed to load</p>';
        });
    }
  }
};

// Theme management
BOMSystem.theme = {
  init() {
    this.applyTheme(BOMSystem.state.theme);
    this.setupThemeToggle();
  },
  
  applyTheme(theme) {
    document.body.setAttribute('data-theme', theme);
    BOMSystem.state.theme = theme;
    localStorage.setItem('bom-theme', theme);
  },
  
  setupThemeToggle() {
    const toggleBtn = BOMSystem.utils.getElement('[data-theme-toggle]');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', () => {
        const newTheme = BOMSystem.state.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
      });
    }
  }
};

// HTMX enhancements
BOMSystem.htmx = {
  init() {
    this.setupEventListeners();
    this.setupProgressIndicators();
    this.setupErrorHandling();
  },
  
  setupEventListeners() {
    // Before request
    document.body.addEventListener('htmx:beforeRequest', (e) => {
      const target = e.target;
      
      // Show loading state
      if (target.hasAttribute('data-loading-text')) {
        target.setAttribute('data-original-text', target.textContent);
        target.textContent = target.getAttribute('data-loading-text');
        target.disabled = true;
      }
      
      // Show global loading
      if (target.hasAttribute('data-global-loading')) {
        BOMSystem.loading.show();
      }
    });
    
    // After request
    document.body.addEventListener('htmx:afterRequest', (e) => {
      const target = e.target;
      
      // Restore button state
      if (target.hasAttribute('data-original-text')) {
        target.textContent = target.getAttribute('data-original-text');
        target.removeAttribute('data-original-text');
        target.disabled = false;
      }
      
      // Hide global loading
      if (target.hasAttribute('data-global-loading')) {
        BOMSystem.loading.hide();
      }
      
      // Handle response status
      if (e.detail.xhr.status >= 400) {
        BOMSystem.notifications.error('An error occurred. Please try again.');
      }
    });
    
    // After swap
    document.body.addEventListener('htmx:afterSwap', (e) => {
      // Re-initialize components for new content
      this.reinitializeComponents(e.detail.target);
      
      // Announce to screen readers
      BOMSystem.accessibility.announceToScreenReader('Content updated');
    });
    
    // Response error
    document.body.addEventListener('htmx:responseError', (e) => {
      BOMSystem.notifications.error('Network error. Please check your connection.');
    });
    
    // Timeout
    document.body.addEventListener('htmx:timeout', (e) => {
      BOMSystem.notifications.warning('Request timed out. Please try again.');
    });
  },
  
  setupProgressIndicators() {
    // Create progress bar
    const progressBar = document.createElement('div');
    progressBar.id = 'htmx-progress';
    progressBar.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 0;
      height: 3px;
      background: var(--secondary-color);
      z-index: 9999;
      transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);
    
    let progressInterval;
    
    document.body.addEventListener('htmx:beforeRequest', () => {
      progressBar.style.width = '0%';
      progressBar.style.opacity = '1';
      
      let progress = 0;
      progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) progress = 90;
        progressBar.style.width = progress + '%';
      }, 100);
    });
    
    document.body.addEventListener('htmx:afterRequest', () => {
      clearInterval(progressInterval);
      progressBar.style.width = '100%';
      
      setTimeout(() => {
        progressBar.style.opacity = '0';
        setTimeout(() => {
          progressBar.style.width = '0%';
        }, 300);
      }, 200);
    });
  },
  
  setupErrorHandling() {
    // Global error handler
    window.addEventListener('error', (e) => {
      console.error('JavaScript error:', e.error);
      BOMSystem.notifications.error('An unexpected error occurred.');
    });
    
    // Unhandled promise rejection
    window.addEventListener('unhandledrejection', (e) => {
      console.error('Unhandled promise rejection:', e.reason);
      BOMSystem.notifications.error('An unexpected error occurred.');
    });
  },
  
  reinitializeComponents(container) {
    // Re-initialize forms
    const forms = container.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
      BOMSystem.forms.setupValidation();
    });
    
    // Re-initialize tables
    const tables = container.querySelectorAll('table[data-sortable]');
    tables.forEach(table => {
      BOMSystem.tables.setupSorting();
    });
    
    // Re-initialize other components as needed
    BOMSystem.forms.setupSearchEnhancements();
    BOMSystem.accessibility.setupScreenReaderSupport();
  }
};

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Initialize all systems
  BOMSystem.notifications.init();
  BOMSystem.forms.init();
  BOMSystem.tables.init();
  BOMSystem.accessibility.init();
  BOMSystem.performance.init();
  BOMSystem.theme.init();
  BOMSystem.htmx.init();
  
  // Add fade-in animation to main content
  const mainContent = BOMSystem.utils.getElement('#main-content');
  if (mainContent) {
    mainContent.classList.add('fade-in');
  }
  
  // Setup mobile menu toggle
  const mobileMenuToggle = BOMSystem.utils.getElement('[data-mobile-menu-toggle]');
  const sidebar = BOMSystem.utils.getElement('.sidebar');
  
  if (mobileMenuToggle && sidebar) {
    mobileMenuToggle.addEventListener('click', () => {
      sidebar.classList.toggle('show');
    });
  }
  
  // Setup tooltips
  if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl);
    });
  }
  
  // Setup popovers
  if (typeof bootstrap !== 'undefined' && bootstrap.Popover) {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
      return new bootstrap.Popover(popoverTriggerEl);
    });
  }
  
  console.log('BOM System UI/UX enhancements initialized');
});

// Export for global access
window.BOMSystem = BOMSystem;

// Service Worker registration for PWA capabilities
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/static/js/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration);
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError);
      });
  });
}

// Performance monitoring
if ('performance' in window) {
  window.addEventListener('load', () => {
    setTimeout(() => {
      const perfData = performance.getEntriesByType('navigation')[0];
      if (perfData) {
        console.log('Page Performance:', {
          'DNS Lookup': perfData.domainLookupEnd - perfData.domainLookupStart,
          'TCP Connection': perfData.connectEnd - perfData.connectStart,
          'Request': perfData.responseStart - perfData.requestStart,
          'Response': perfData.responseEnd - perfData.responseStart,
          'DOM Processing': perfData.domContentLoadedEventEnd - perfData.responseEnd,
          'Total Load Time': perfData.loadEventEnd - perfData.navigationStart
        });
      }
    }, 0);
  });
}

// Memory usage monitoring (development only)
if (process?.env?.NODE_ENV === 'development' && 'memory' in performance) {
  setInterval(() => {
    const memory = performance.memory;
    if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.9) {
      console.warn('High memory usage detected:', {
        used: Math.round(memory.usedJSHeapSize / 1024 / 1024) + 'MB',
        total: Math.round(memory.totalJSHeapSize / 1024 / 1024) + 'MB',
        limit: Math.round(memory.jsHeapSizeLimit / 1024 / 1024) + 'MB'
      });
    }
  }, 30000);
}