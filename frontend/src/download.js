import apiClient from './axios';

export const download = async (role, id) => {
    let url = '';
    if (role === 'Admin') {
        url = '/api/v1/downloads/report';
    } else if (role === 'Student') {
        url = `/api/v1/downloads/student/${id}/report`;
    } else if (role === 'Company') {
        url = `/api/v1/downloads/company/${id}/report`;
    } else if (role === 'Drive') {
        url = `/api/v1/downloads/drive/${id}/report`;
    } else if (role === 'Placement') {
        url = `/api/v1/downloads/placement/${id}/report`;
    } else {
        console.error("Invalid Role");
        return;
    }

    try {
        const res = await apiClient.get(url);
        poll(res.data.id, 1000);
    } catch (e) {
        console.error(e);
    }
}

const poll = async (id, delay) => {
    try {
        const res = await apiClient.get(`/api/v1/downloads/${id}`, {
            responseType: 'blob'
        });
        if (res.status === 200) {
            const url = window.URL.createObjectURL(new Blob([res.data]));
            const link = document.createElement('a');
            link.href = url;
            
            const contentDisposition = res.headers['content-disposition'];
            let fileName = 'report.pdf';
            if (contentDisposition) {
                const fileNameMatch = contentDisposition.match(/filename="?(.+)"?/);
                if (fileNameMatch.length === 2)
                    fileName = fileNameMatch[1];
            }
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
            link.remove();
        } else if (res.status === 202) {
            setTimeout(() => poll(id, delay * 2), delay);
        }
    } catch (e) {
        console.error(e);
    }
}