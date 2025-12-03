

// add for sec home to p
function typeWriter() {
    let p = document.getElementById('pro');
    if (!p) return;
    
    let text = p.dataset.text;
    let i = 0;
      
    p.textContent = '';
    
    let id = setInterval(function() {
        p.textContent += text[i];
        i++;
        if(i >= text.length) {
            clearInterval(id);
        }
    }, 20);
}

document.addEventListener('DOMContentLoaded', typeWriter);

// add for nav
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.getElementById('headers');
    
    if (nav) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 20) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });
        
        if (window.scrollY > 20) {
            nav.classList.add('scrolled');
        }
    }
});
//   let menu=document.querySelector(".nav-links , .nav-btn");
// document.querySelector('#menu-icon').onclick = () =>{
//     menu.classList.toggle('menu-open')
// }
document.addEventListener('DOMContentLoaded', function() {
    const menuIcon = document.getElementById('menu-icon');
    const navLinks = document.querySelector('.nav-links');
    const navBtn = document.querySelector('.nav-btn');
    const navLinksItems = document.querySelectorAll('.nav-link');
    
    // حساب ارتفاع القائمة
    function updateMenuHeight() {
        if (navLinks.classList.contains('active')) {
            const height = navLinks.scrollHeight;
            document.documentElement.style.setProperty('--menu-height', height + 'px');
        }
    }
    
    // فتح/إغلاق القائمة
    menuIcon.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        navBtn.classList.toggle('active');
        
        if (navLinks.classList.contains('active')) {
            updateMenuHeight();
            // تغيير الأيقونة إلى إغلاق
            menuIcon.classList.remove('fa-bars');
            menuIcon.classList.add('fa-times');
        } else {
            // إزالة الارتفاع
            document.documentElement.style.removeProperty('--menu-height');
            // إعادة الأيقونة إلى القائمة
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    });
    
    // إغلاق القائمة عند النقر على رابط
    navLinksItems.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
            navBtn.classList.remove('active');
            document.documentElement.style.removeProperty('--menu-height');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        });
    });
    
    // إغلاق القائمة عند التمرير
    window.addEventListener('scroll', function() {
        if (navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            navBtn.classList.remove('active');
            document.documentElement.style.removeProperty('--menu-height');
            menuIcon.classList.remove('fa-times');
            menuIcon.classList.add('fa-bars');
        }
    });
});
// forgot password form
document.addEventListener('DOMContentLoaded', function() {
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('email').value;
            const successAlert = document.getElementById('successAlert');
            const errorAlert = document.getElementById('errorAlert');
            
            // إخفاء جميع التنبيهات أولاً
            successAlert.style.display = 'none';
            errorAlert.style.display = 'none';
            
            if (email && email.includes('@')) {
                successAlert.style.display = 'block';
                document.getElementById('email').value = '';
            } else {
                errorAlert.style.display = 'block';
            }
        });
    }

    // كود تبديل الأقسام - نسخة واحدة فقط
    const tabLinks = document.querySelectorAll('.tab-link');
    
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // إزالة النشاط من كل الروابط
            tabLinks.forEach(tab => tab.classList.remove('active'));
            
            // إضافة النشاط للرابط المختار
            this.classList.add('active');
            
            // إخفاء كل الأقسام
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(section => section.classList.remove('active'));
            
            // إظهار القسم المختار
            const targetTab = this.getAttribute('data-tab');
            const targetSection = document.getElementById(targetTab);
            if (targetSection) {
                targetSection.classList.add('active');
            }
        });
    });
});

