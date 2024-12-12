import React, { useState } from 'react';

function AdminMovieFilesPage() {
    const [movieId, setMovieId] = useState('');
    const [file, setFile] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

    const handleUpload = async (e) => {
        e.preventDefault();
        if (!movieId || !file) {
            setError('Please provide both movie ID and a file.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        const formData = new FormData();
        formData.append('movie_file', file);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/admin/movie-s3/${movieId}/upload`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to upload movie file');
            }

            setSuccessMessage('Movie file uploaded successfully!');
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDelete = async () => {
        if (!movieId) {
            setError('Please provide a movie ID.');
            return;
        }

        setIsLoading(true);
        setError(null);
        setSuccessMessage(null);

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/admin/movie-s3/${movieId}/delete`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to delete movie file');
            }

            setSuccessMessage('Movie file deleted successfully!');
        } catch (err) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="homepage">
            <header className="homepage-header">
                <h1>Manage Movie Files (S3)</h1>
            </header>

            {isLoading && <p style={{ textAlign: 'center', color: '#007bff' }}>Processing...</p>}
            {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
            {successMessage && <p style={{ color: 'green', textAlign: 'center' }}>{successMessage}</p>}

            <section style={{ marginTop: '20px', textAlign: 'center' }}>
                <h2>Upload Movie File</h2>
                <form onSubmit={handleUpload} style={{ display: 'inline-block', textAlign: 'left' }}>
                    <div style={{ marginBottom: '10px' }}>
                        <label>Movie ID:</label><br/>
                        <input
                            type="text"
                            value={movieId}
                            onChange={(e) => setMovieId(e.target.value)}
                            style={{ width: '300px', padding: '5px' }}
                            required
                        />
                    </div>
                    <div style={{ marginBottom: '10px' }}>
                        <label>File:</label><br/>
                        <input
                            type="file"
                            onChange={(e) => setFile(e.target.files[0])}
                            style={{ width: '300px', padding: '5px' }}
                            required
                        />
                    </div>
                    <button
                        type="submit"
                        style={{
                            padding: '10px 20px',
                            fontSize: '16px',
                            backgroundColor: '#007bff',
                            color: '#fff',
                            border: 'none',
                            cursor: 'pointer',
                            marginRight: '10px'
                        }}
                    >
                        Upload
                    </button>
                </form>

                <h2 style={{ marginTop: '40px' }}>Delete Movie File</h2>
                <div style={{ marginBottom: '10px', display: 'inline-block', textAlign: 'left' }}>
                    <label>Movie ID:</label><br/>
                    <input
                        type="text"
                        value={movieId}
                        onChange={(e) => setMovieId(e.target.value)}
                        style={{ width: '300px', padding: '5px' }}
                    />
                </div>
                <br/>
                <button
                    onClick={handleDelete}
                    style={{
                        padding: '10px 20px',
                        fontSize: '16px',
                        backgroundColor: '#dc3545',
                        color: '#fff',
                        border: 'none',
                        cursor: 'pointer',
                        marginTop: '10px'
                    }}
                >
                    Delete
                </button>

            </section>

            <footer className="homepage-footer">
                <p>© 2024 Online Cinema. All rights reserved.</p>
            </footer>
        </div>
    );
}

export default AdminMovieFilesPage;
