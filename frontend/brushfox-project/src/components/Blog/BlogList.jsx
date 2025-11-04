import BlogCard from './BlogCard';
import Loading from '../Common/Loading';
import ErrorMessage from '../Common/ErrorMessage';
import './BlogList.css';

const BlogList = ({ posts, loading, error, onRetry }) => {
  if (loading) return <Loading message="Ładowanie postów..." />;
  if (error) return <ErrorMessage message={error} onRetry={onRetry} />;
  if (!posts || posts.length === 0) {
    return (
      <div className="no-posts">
        <p>Brak postów do wyświetlenia.</p>
      </div>
    );
  }

  return (
    <div className="blog-list">
      {posts.map((post) => (
        <BlogCard key={post.id} post={post} />
      ))}
    </div>
  );
};

export default BlogList;
