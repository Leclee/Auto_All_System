let allAccounts = [];

document.addEventListener('DOMContentLoaded', () => {
    fetchAccounts();
    
    document.getElementById('searchInput').addEventListener('input', renderTable);
    document.querySelectorAll('.filter-cb').forEach(cb => cb.addEventListener('change', renderTable));
    
    // 全选/取消全选
    document.getElementById('selectAll').addEventListener('change', function() {
        document.querySelectorAll('.row-checkbox').forEach(cb => cb.checked = this.checked);
    });
    
    // 按钮事件
    document.getElementById('btnImport').addEventListener('click', showImportModal);
    document.getElementById('btnDelete').addEventListener('click', deleteSelected);
    document.getElementById('btnExport').addEventListener('click', showExportModal);
    document.getElementById('btnConfirmExport').addEventListener('click', confirmExport);
    document.getElementById('btnCancelExport').addEventListener('click', hideExportModal);
    document.getElementById('btnConfirmImport').addEventListener('click', confirmImport);
    document.getElementById('btnCancelImport').addEventListener('click', hideImportModal);
    
    // 分隔符选择器事件
    document.getElementById('importSeparator').addEventListener('change', function() {
        const customInput = document.getElementById('customSeparator');
        if (this.value === 'custom') {
            customInput.style.display = 'inline-block';
            customInput.focus();
        } else {
            customInput.style.display = 'none';
        }
    });
});

function fetchAccounts() {
    fetch('/api/accounts')
        .then(r => r.json())
        .then(data => {
            allAccounts = data;
            renderTable();
        })
        .catch(err => {
            console.error('加载数据失败:', err);
            document.getElementById('countDisplay').innerText = '加载失败，请检查后台服务';
        });
}

function renderTable() {
    const tbody = document.getElementById('accountTableBody');
    tbody.innerHTML = '';
    
    const search = document.getElementById('searchInput').value.toLowerCase();
    const activeStatues = Array.from(document.querySelectorAll('.filter-cb:checked')).map(cb => cb.value);
    
    const filtered = allAccounts.filter(acc => {
        if (activeStatues.length > 0 && !activeStatues.includes(acc.status)) return false;
        
        const term = search;
        if (!term) return true;
        
        return (acc.email || '').toLowerCase().includes(term) || 
               (acc.status || '').toLowerCase().includes(term);
    });
    
    document.getElementById('countDisplay').innerText = `显示 ${filtered.length} / ${allAccounts.length} 个账号`;

    filtered.forEach(acc => {
        const tr = document.createElement('tr');
        
        // 创建可点击复制的单元格
        tr.innerHTML = `
            <td><input type="checkbox" class="row-checkbox" data-email="${acc.email || ''}"></td>
            <td class="copyable" data-value="${acc.email || ''}">${acc.email || '-'}</td>
            <td class="copyable" data-value="${acc.password || ''}">${acc.password || '-'}</td>
            <td class="copyable" data-value="${acc.recovery_email || ''}">${acc.recovery_email || '-'}</td>
            <td class="copyable" data-value="${acc.secret_key || ''}">${acc.secret_key || '-'}</td>
            <td class="copyable link-cell" data-value="${acc.verification_link || ''}" title="${acc.verification_link || ''}">${acc.verification_link || '-'}</td>
            <td><span class="status-badge status-${acc.status}">${mapStatus(acc.status)}</span></td>
        `;
        tbody.appendChild(tr);
    });
    
    // 为所有可复制单元格添加点击事件
    document.querySelectorAll('.copyable').forEach(cell => {
        cell.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            if (value && value !== '-' && value !== '') {
                copyToClipboard(value);
                showCopyFeedback(this);
            }
        });
    });
    
    window.currentFiltered = filtered; // For export
}

function copyToClipboard(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            console.log('已复制到剪贴板');
        }).catch(err => {
            console.error('复制失败:', err);
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
}

function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    try {
        document.execCommand('copy');
        console.log('已复制（兼容模式）');
    } catch (err) {
        console.error('复制失败:', err);
    }
    document.body.removeChild(textarea);
}

function showCopyFeedback(element) {
    const originalBg = element.style.backgroundColor;
    element.style.backgroundColor = '#d4edda';
    element.style.transition = 'background-color 0.2s';
    setTimeout(() => {
        element.style.backgroundColor = originalBg;
    }, 500);
}

function mapStatus(s) {
    const map = {
        'pending_check': '待检测资格',
        'link_ready': '有资格待验证已提取链接',
        'verified': '已验证未绑卡',
        'subscribed': '已绑卡订阅',
        'ineligible': '无资格',
        'error': '错误/超时'
    };
    return map[s] || s;
}

function showExportModal() {
    document.getElementById('exportModal').style.display = 'block';
}

function hideExportModal() {
    document.getElementById('exportModal').style.display = 'none';
}

function confirmExport() {
    if (!window.currentFiltered || window.currentFiltered.length === 0) {
        alert("没有可导出的账号！");
        return;
    }
    
    const fields = Array.from(document.querySelectorAll('.export-field:checked')).map(cb => cb.value);
    const emails = window.currentFiltered.map(acc => acc.email);
    
    fetch('/api/export', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({emails, fields})
    })
    .then(res => res.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `exported_accounts_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        hideExportModal();
    })
    .catch(err => {
        console.error('导出失败:', err);
        alert('导出失败，请查看控制台日志');
    });
}

// 删除选中的账号
function deleteSelected() {
    const checked = Array.from(document.querySelectorAll('.row-checkbox:checked'));
    if (checked.length === 0) {
        alert('请先选择要删除的账号！');
        return;
    }
    
    if (!confirm(`确定要删除选中的 ${checked.length} 个账号吗？此操作不可撤销！`)) {
        return;
    }
    
    const emails = checked.map(cb => cb.getAttribute('data-email'));
    
    fetch('/api/delete', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({emails})
    })
    .then(res => res.json())
    .then(data => {
        alert(`成功删除 ${data.deleted} 个账号`);
        fetchAccounts(); // 重新加载
    })
    .catch(err => {
        console.error('删除失败:', err);
        alert('删除失败，请查看控制台日志');
    });
}

// 显示导入模态框
function showImportModal() {
    document.getElementById('importModal').style.display = 'block';
}

// 隐藏导入模态框
function hideImportModal() {
    document.getElementById('importModal').style.display = 'none';
    document.getElementById('importText').value = '';
}

// 确认导入
function confirmImport() {
    const text = document.getElementById('importText').value.trim();
    if (!text) {
        alert('请输入账号信息！');
        return;
    }
    
    let separator = document.getElementById('importSeparator').value;
    
    // 如果选择了自定义，使用自定义输入框的值
    if (separator === 'custom') {
        separator = document.getElementById('customSeparator').value;
        if (!separator) {
            alert('请输入自定义分隔符！');
            return;
        }
    }
    
    const status = document.getElementById('importStatus').value;
    
    fetch('/api/import', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({accounts: text, separator, status})
    })
    .then(res => res.json())
    .then(data => {
        alert(`成功导入 ${data.imported} 个账号`);
        hideImportModal();
        fetchAccounts(); // 重新加载
    })
    .catch(err => {
        console.error('导入失败:', err);
        alert('导入失败，请查看控制台日志');
    });
}
