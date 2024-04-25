function [rotcorr, rrcorr] = fast_cross_correlation(rois, rrois, dim, forty)
    angles = rotation_xyz(dim, forty);
    n = size(rois, 2);

    % Calculate mean and difference once for all iterations
    mean_rois = mean(rois);
    t_mean_mat = ones(size(rois, 1), 1) * mean_rois;
    n_sum = rois - t_mean_mat;
    d_sum = sqrt(sum(n_sum.^2));

    rmean_rois = mean(rrois);
    rt_mean_mat = ones(size(rrois, 1), 1) * rmean_rois;
    rn_sum = rrois - rt_mean_mat;
    rd_sum = sqrt(sum(rn_sum.^2));

    % Preallocate memory
    corr = zeros(n, n, 'single');
    rcorr = zeros(n, n, 'single');

    % Loop over each seed
    for i = 1:n
        nseed = n_sum(:, i);
        dseed = d_sum(i);
        rnseed = rn_sum(:, i);
        rdseed = rd_sum(i);
        
        % Create rotated versions of the seed
        nto_be_cor = nseed(angles(:));
        rnto_be_cor = rnseed(angles(:));

        % Loop over targets
        for j = (i+1):n
            ntarget = n_sum(:, j);
            dtarget = d_sum(j);
            rntarget = rn_sum(:, j);
            rdtarget = rd_sum(j);
            
            % Calculate correlations
            tr = sum(nto_be_cor .* (ntarget * ones(1, numel(angles)))) / (dseed * dtarget);
            rtr = sum(rnto_be_cor .* (rntarget * ones(1, numel(angles)))) / (rdseed * rdtarget);
            
            % Store correlations
            corr(i, j) = max(tr);
            rcorr(i, j) = max(rtr);
        end
    end

    % Sum with transpose to fill the lower triangle of the correlation matrices
    rotcorr = corr + permute(corr, [2, 1, 3]);
    rrcorr = rcorr + permute(rcorr, [2, 1, 3]);
end