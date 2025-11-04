import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import useFetch from '../hooks/useFetch';
import { apiService } from '../services/api';
import BlogList from '../components/Blog/BlogList';
import Button from '../components/Common/Button';
import './Blog.css';

const Blog = () => {
  const { isAuthenticated } = useAuth();
  const { data, loading, error, refetch } = useFetch(() => apiService.getPosts());

  // Handle paginated response
  const posts = data?.results || data || [];

  return (
    <div className="blog-page">
      <div className="page-header">
        <h1>Blog</h1>
        <p className="page-subtitle">Moje przemyślenia, porady i historie</p>
        {isAuthenticated && (
          <Link to="/blog/new">
            <Button>✍️ Dodaj nowy post</Button>
          </Link>
        )}
      </div>

      <BlogList 
        posts={posts} 
        loading={loading} 
        error={error} 
        onRetry={refetch}
      />
    </div>
  );
};

export default Blog;
