package github_files_provider

import (
	"io"

	"github.com/subtle-byte/ghloc/internal/service/github_stat"
)

// It is like io.LimitedReader but returns model.BadRequest when Remaining == 0
type LimitedReader struct {
	Reader    io.Reader
	Remaining int
}

func (r *LimitedReader) Read(p []byte) (n int, err error) {
	if r.Remaining <= 0 {
		return 0, github_stat.ErrRepoTooLarge
	}
	if len(p) > r.Remaining {
		p = p[0:r.Remaining]
	}
	n, err = r.Reader.Read(p)
	r.Remaining -= n
	return
}
