document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');

    if (sidebar) {
        let isResizing = false;

        const resizer = document.createElement('div');
        resizer.style.width = '5px';
        resizer.style.height = '100%';
        resizer.style.position = 'absolute';
        resizer.style.right = '0';
        resizer.style.top = '0';
        resizer.style.cursor = 'col-resize';
        sidebar.appendChild(resizer);

        resizer.addEventListener('mousedown', function(e) {
            isResizing = true;
            document.addEventListener('mousemove', handleMouseMove);
            document.addEventListener('mouseup', function() {
                isResizing = false;
                document.removeEventListener('mousemove', handleMouseMove);
            });
        });

        function handleMouseMove(e) {
            if (!isResizing) {
                return;
            }

            const newWidth = e.clientX;
            if (newWidth > 200 && newWidth < 500) { // Set min and max width
                sidebar.style.width = newWidth + 'px';
                mainContent.style.marginLeft = newWidth + 'px';
                localStorage.setItem('sidebarWidth', newWidth);
            }
        }

        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth) {
            sidebar.style.width = savedWidth + 'px';
            mainContent.style.marginLeft = savedWidth + 'px';
        }
    }
});
